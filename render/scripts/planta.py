# -*- coding: utf-8 -*-
"""
Utilidades para planos de distribución a escala con áreas verificadas.
Requiere: shapely  (pip install shapely --break-system-packages)

Convención de coordenadas: metros, origen en la esquina superior izquierda,
x hacia la derecha, y hacia abajo. Coincide con el sistema de coordenadas SVG,
así que el plano en pantalla sale igual que las coordenadas.
"""
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely.prepared import prep


# ---------------------------------------------------------------- geometría
def area_poligono(pts):
    """Área por fórmula del zapatero. Úsala para validar el levantamiento."""
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def perimetro(pts):
    import math
    t = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        t += math.hypot(x2 - x1, y2 - y1)
    return t


class Planta:
    """Contorno + obstáculos + zonas, con verificación."""

    def __init__(self, contorno, obstaculos=(), ventanales=(), area_declarada=None):
        self.cont = Polygon(contorno)
        self.obst = [box(x, y, x + w, y + h) for (x, y, w, h) in obstaculos]
        self.ventanales = list(ventanales)   # [(x0, x1, y), ...] tramos de vidrio
        self.util = self.cont
        for o in self.obst:
            self.util = self.util.difference(o)
        if area_declarada is not None:
            d = abs(self.cont.area - area_declarada)
            if d > 0.5:
                raise ValueError(
                    f"El área calculada ({self.cont.area:.2f} m²) no coincide con la "
                    f"declarada ({area_declarada:.2f} m²): diferencia {d:.2f} m². "
                    "Revisa las cotas antes de seguir.")

    @property
    def area_bruta(self):  return self.cont.area
    @property
    def area_util(self):   return self.util.area

    def verificar(self, zonas):
        """zonas: lista de dicts con 'n' (nombre) y 'r' = (x, y, w, h).
        Lanza AssertionError si algo se sale o se solapa. Devuelve el área de cada una."""
        rects = [box(z["r"][0], z["r"][1], z["r"][0] + z["r"][2], z["r"][1] + z["r"][3])
                 for z in zonas]
        for i, r in enumerate(rects):
            fuera = r.difference(self.cont).area
            assert fuera < 0.05, (
                f"«{zonas[i]['n']}» se sale del contorno en {fuera:.2f} m²")
            for j in range(i + 1, len(rects)):
                ov = r.intersection(rects[j]).area
                assert ov < 0.05, (
                    f"«{zonas[i]['n']}» y «{zonas[j]['n']}» se solapan {ov:.2f} m²")
        for z, r in zip(zonas, rects):
            z["a"] = r.intersection(self.util).area
        return zonas

    def abierta(self, zonas, excluir=()):
        """Área libre tras descontar las zonas cerradas y los rectángulos de `excluir`
        (típicamente el barrido de la puerta y el corredor de entrada)."""
        rects = [box(z["r"][0], z["r"][1], z["r"][0] + z["r"][2], z["r"][1] + z["r"][3])
                 for z in zonas]
        libre = self.util.difference(unary_union(rects)) if rects else self.util
        for (x, y, w, h) in excluir:
            libre = libre.difference(box(x, y, x + w, y + h))
        return libre

    def ventanal_libre(self, zonas):
        """Metros de ventanal que NO quedan tapados, y los tramos sueltos que resultan.
        Un tramo de menos de 2.5 m no sirve para una fila de puestos: avísalo."""
        out = []
        for (x0, x1, yv) in self.ventanales:
            corte = []
            for z in zonas:
                zx, zy, zw, zh = z["r"]
                if abs(zy - yv) < 0.06 or (zy < yv < zy + zh):
                    a, b = max(zx, x0), min(zx + zw, x1)
                    if b > a:
                        corte.append((a, b))
            corte.sort()
            libres, cur = [], x0
            for (a, b) in corte:
                if a > cur:
                    libres.append((cur, a))
                cur = max(cur, b)
            if cur < x1:
                libres.append((cur, x1))
            out.extend(libres)
        total = sum(b - a for (a, b) in out)
        return total, out


# ---------------------------------------------------------------- mobiliario
SILLA = 0.78          # profundidad que ocupa una silla retirada de la mesa
PASILLO = 1.15        # entre módulos de mobiliario

# (ancho, fondo, plazas) — sillas en los dos lados largos
MODULOS = [(3.20, 1.40, 8), (2.40, 1.40, 6), (1.60, 1.40, 4)]
INDIVIDUAL = (1.50, 0.75, 1)


def empacar(libre, modulos=MODULOS, individual=INDIVIDUAL,
            silla=SILLA, pasillo=PASILLO, paso=0.25, offsets=5, limites=(14.56, 9.41)):
    """Coloca mobiliario dentro de `libre` respetando pasillos reales.
    Devuelve la lista de módulos colocados; suma sus 'pl' para el conteo de plazas.

    El conteo que sale de aquí es el número que se entrega: son las sillas que
    de verdad caben, no una estimación por m²/puesto."""
    LX, LY = limites
    base = []
    for (w, d, pl) in modulos:
        base.append((w, d + 2 * silla, pl, False))
        base.append((d + 2 * silla, w, pl, True))
    w, d, pl = individual
    ind = [(w, d + silla, pl, False), (d + silla, w, pl, True)]

    P = prep(libre)

    def corrida(cands, ox, oy):
        ocup, out = [], []
        for (fw, fh, pl_, rot) in cands:
            y = oy
            while y + fh <= LY:
                x = ox
                while x + fw <= LX:
                    f = box(x + .02, y + .02, x + fw - .02, y + fh - .02)
                    if P.contains(f):
                        g = (x - pasillo / 2, y - pasillo / 2,
                             x + fw + pasillo / 2, y + fh + pasillo / 2)
                        if not any(not (g[2] <= o[0] or g[0] >= o[2] or
                                        g[3] <= o[1] or g[1] >= o[3]) for o in ocup):
                            ocup.append((x, y, x + fw, y + fh))
                            out.append(dict(x=x, y=y, fw=fw, fh=fh, pl=pl_, rot=rot))
                    x += paso
                y += paso
        return out

    best = []
    for cands in (base + ind, base[::-1] + ind):
        for i in range(offsets):
            for j in range(offsets):
                r = corrida(cands, round(j * paso, 2), round(i * paso, 2))
                if sum(m["pl"] for m in r) > sum(m["pl"] for m in best):
                    best = r
    return best


# ---------------------------------------------------------------- SVG
class Lienzo:
    """Dibuja el plano. Todos los colores salen de variables CSS para que el
    artifact funcione en tema claro y oscuro sin tocar el SVG."""

    def __init__(self, ancho, alto, escala=54.0, margen=48):
        self.W, self.H, self.M, self.P = ancho, alto, escala, margen
        self.o = []

    def X(self, v): return v * self.M + self.P
    def Y(self, v): return v * self.M + self.P

    def abrir(self, etiqueta="Plano de distribución"):
        vw = self.W * self.M + self.P * 2
        vh = self.H * self.M + self.P * 2
        self.o.append(
            f'<svg viewBox="0 0 {vw:.0f} {vh:.0f}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{etiqueta}" class="plano">')
        self.o.append(
            '<defs><pattern id="hx" width="6" height="6" patternTransform="rotate(45)" '
            'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" '
            'stroke="var(--wall)" stroke-width="2.2"/></pattern></defs>')

    def suelo(self, contorno):
        self.pts = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in contorno)
        self.o.append(f'<polygon points="{self.pts}" fill="var(--floor)"/>')

    def zona(self, x, y, w, h, color, op=0.18):
        self.o.append(
            f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{w*self.M:.1f}" '
            f'height="{h*self.M:.1f}" fill="{color}" fill-opacity="{op}" '
            f'stroke="{color}" stroke-width="1.8"/>')

    def mesa(self, x, y, w, h, fill="var(--desk)"):
        self.o.append(
            f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{w*self.M:.1f}" '
            f'height="{h*self.M:.1f}" rx="3" fill="{fill}" stroke="var(--deskLn)" '
            'stroke-width="1.2"/>')

    def silla(self, cx, cy):
        self.o.append(
            f'<circle cx="{self.X(cx):.1f}" cy="{self.Y(cy):.1f}" '
            f'r="{0.235*self.M:.1f}" fill="none" stroke="var(--deskLn)" stroke-width="1.2"/>')

    def modulo(self, m, silla_p=SILLA):
        """Dibuja un módulo devuelto por empacar(): mesa + sus sillas."""
        x, y, fw, fh, pl, rot = m["x"], m["y"], m["fw"], m["fh"], m["pl"], m["rot"]
        if pl == 1:
            if rot:
                self.mesa(x + silla_p, y, fw - silla_p, fh)
                self.silla(x + silla_p - 0.36, y + fh / 2)
            else:
                self.mesa(x, y + silla_p, fw, fh - silla_p)
                self.silla(x + fw / 2, y + silla_p - 0.36)
            return
        n = pl // 2
        if rot:
            mw, md = fw - 2 * silla_p, fh
            self.mesa(x + silla_p, y, mw, md)
            for k in range(n):
                cy = y + md * (k + 0.5) / n
                self.silla(x + silla_p - 0.36, cy)
                self.silla(x + silla_p + mw + 0.36, cy)
        else:
            mw, md = fw, fh - 2 * silla_p
            self.mesa(x, y + silla_p, mw, md)
            for k in range(n):
                cx = x + mw * (k + 0.5) / n
                self.silla(cx, y + silla_p - 0.36)
                self.silla(cx, y + silla_p + md + 0.36)

    def muros(self):
        self.o.append(
            f'<polygon points="{self.pts}" fill="none" stroke="var(--wall)" '
            'stroke-width="5" stroke-linejoin="miter" pointer-events="none"/>')

    def ventanal(self, x0, x1, y):
        self.o.append(
            f'<line x1="{self.X(x0):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(x1):.1f}" '
            f'y2="{self.Y(y):.1f}" stroke="var(--glass)" stroke-width="7"/>')
        self.o.append(
            f'<line x1="{self.X(x0):.1f}" y1="{self.Y(y)-4:.1f}" x2="{self.X(x1):.1f}" '
            f'y2="{self.Y(y)-4:.1f}" stroke="var(--glass)" stroke-width="1.6"/>')

    def columna(self, x, y, w, h):
        self.o.append(
            f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{w*self.M:.1f}" '
            f'height="{h*self.M:.1f}" fill="url(#hx)" stroke="var(--wall)" stroke-width="2.5"/>')

    def puerta(self, x, y, ancho=0.90, gozne="izq", hacia="arriba", color="var(--ink)"):
        """Hoja + barrido. `gozne` dice de qué lado está el eje de giro."""
        M = self.M
        gx = x if gozne == "izq" else x + ancho
        dy = -ancho if hacia == "arriba" else ancho
        sweep = 1 if (gozne == "izq") == (hacia == "arriba") else 0
        self.o.append(
            f'<line x1="{self.X(x):.1f}" y1="{self.Y(y):.1f}" '
            f'x2="{self.X(x+ancho):.1f}" y2="{self.Y(y):.1f}" '
            'stroke="var(--floor)" stroke-width="6"/>')
        self.o.append(
            f'<path d="M {self.X(gx):.1f} {self.Y(y):.1f} A {ancho*M:.1f} {ancho*M:.1f} '
            f'0 0 {sweep} {self.X(gx):.1f} {self.Y(y)+dy*M:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        self.o.append(
            f'<line x1="{self.X(gx):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(gx):.1f}" '
            f'y2="{self.Y(y)+dy*M:.1f}" stroke="{color}" stroke-width="2.2"/>')

    def etiqueta(self, x, y, w, h, texto, area, color, dy=0):
        """`texto` admite varias líneas separadas por |. Rota si la zona es vertical."""
        cx, cy = self.X(x + w / 2), self.Y(y + h / 2)
        lines = texto.split("|")
        tr = (f' transform="rotate(-90 {cx:.1f} {cy:.1f})"' if h > w * 1.45 else '')
        self.o.append(f'<g{tr}>')
        for i, ln in enumerate(lines):
            cls = "zl" if i == 0 else "zs"
            self.o.append(
                f'<text x="{cx:.1f}" y="{cy-8+i*12+dy:.1f}" text-anchor="middle" '
                f'class="{cls}" fill="{color}">{ln}</text>')
        self.o.append(
            f'<text x="{cx:.1f}" y="{cy-8+len(lines)*12+3+dy:.1f}" text-anchor="middle" '
            f'class="za" fill="{color}">{area:.1f} m²</text>')
        self.o.append('</g>')

    def cota(self, x1, y1, x2, y2, texto, vertical=False):
        self.o.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            'stroke="var(--dim)" stroke-width="1"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        tr = f' transform="rotate(-90 {mx:.1f} {my:.1f})"' if vertical else ''
        self.o.append(
            f'<text x="{mx:.1f}" y="{my-6:.1f}" text-anchor="middle" class="ct"{tr}>{texto}</text>')

    def nota(self, x, y, texto, color="var(--muted)"):
        self.o.append(
            f'<text x="{self.X(x):.1f}" y="{self.Y(y):.1f}" class="mb" fill="{color}">{texto}</text>')

    def cerrar(self):
        self.o.append('</svg>')
        return "\n".join(self.o)


PALETA_ZONAS = {
    "reunion":  "#2F6F94",
    "redes":    "#B44B38",
    "privada":  "#6B5892",
    "servicio": "#A87B2C",
    "abierta":  "#4E7C4A",
    "deposito": "#7A6A58",
    "otro":     "#5C6670",
}
