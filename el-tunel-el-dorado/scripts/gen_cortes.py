# -*- coding: utf-8 -*-
"""Cortes (secciones) técnicos del módulo sanitario, en el mismo lenguaje visual
del plano (papel técnico, cotas monoespaciadas). Elevación: eje horizontal = la
coordenada de planta que se corta, eje vertical = altura Z."""

ANCHO, FONDO, TAB = 9.83, 5.00, 0.15
MOD_W = (ANCHO - TAB) / 2   # 4.84
X0 = MOD_W + TAB            # 4.99
ALT = 2.80

M = 64.0    # px por metro, igual que el plano
P = 56.0    # margen

class Corte:
    def __init__(self, x_lo, x_hi, z_lo=-0.55, z_hi=ALT+1.05):
        self.x_lo, self.x_hi, self.z_lo, self.z_hi = x_lo, x_hi, z_lo, z_hi
        self.o = []

    def X(self, v): return (v - self.x_lo) * M + P
    def Z(self, v): return (self.z_hi - v) * M + P   # Z crece hacia arriba en el dibujo

    def rect(self, x, z, w, h, fill, stroke="var(--wall)", sw=1.4, op=1):
        self.o.append(f'<rect x="{self.X(x):.1f}" y="{self.Z(z+h):.1f}" width="{w*M:.1f}" '
                       f'height="{h*M:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')

    def linea(self, x1, z1, x2, z2, stroke="var(--dim)", w=1, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<line x1="{self.X(x1):.1f}" y1="{self.Z(z1):.1f}" x2="{self.X(x2):.1f}" '
                       f'y2="{self.Z(z2):.1f}" stroke="{stroke}" stroke-width="{w}"{d}/>')

    def cota_v(self, x, z1, z2, texto):
        self.linea(x, z1, x, z2, "var(--dim)", 1)
        self.linea(x-0.05, z1, x+0.05, z1, "var(--dim)", 1)
        self.linea(x-0.05, z2, x+0.05, z2, "var(--dim)", 1)
        mx, my = self.X(x)+8, self.Z((z1+z2)/2)
        self.o.append(f'<text x="{mx:.1f}" y="{my:.1f}" class="ct" dominant-baseline="middle">{texto}</text>')

    def cota_h(self, x1, x2, z, texto):
        self.linea(x1, z, x2, z, "var(--dim)", 1)
        self.linea(x1, z-0.05, x1, z+0.05, "var(--dim)", 1)
        self.linea(x2, z-0.05, x2, z+0.05, "var(--dim)", 1)
        my = self.Z(z) - 6
        mx = self.X((x1+x2)/2)
        self.o.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" class="ct">{texto}</text>')

    def texto(self, x, z, txt, cls="mb", anchor="middle", fill="var(--muted)"):
        self.o.append(f'<text x="{self.X(x):.1f}" y="{self.Z(z):.1f}" text-anchor="{anchor}" '
                       f'class="{cls}" fill="{fill}">{txt}</text>')

    def cerrar(self, etiqueta):
        vw = (self.x_hi - self.x_lo) * M + P * 2
        vh = (self.z_hi - self.z_lo) * M + P * 2
        head = (f'<svg viewBox="0 0 {vw:.0f} {vh:.0f}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" aria-label="{etiqueta}" class="plano">')
        return head + "".join(self.o) + "</svg>"


def franja_abierta(c, x1, x2, z=ALT):
    c.linea(x1, z, x2, z, "var(--wall)", 2, dash="3 3")
    n = max(1, int((x2-x1)/0.3))
    for i in range(n+1):
        xx = x1 + i*0.3
        c.linea(xx, z, min(xx+0.18, x2), z+0.30, "var(--dim)", 0.8)


# ============================================================ CORTE A-A (transversal, y=3.00)
def corte_AA():
    c = Corte(-0.5, ANCHO+1.1)
    c.rect(-0.5, -0.05, ANCHO+1.0, 0.05, "var(--floor)", "none")
    c.linea(-0.5, 0, ANCHO+0.5, 0, "var(--wall)", 2)
    c.rect(-0.15, 0, 0.15, ALT, "var(--wall)")
    c.rect(0, 0.46, 0.55, 0.30, "#585650")
    c.rect(0, 0.76, 0.55, 0.05, "#6b6862")
    c.rect(0, 0.90, 0.02, 0.95, "var(--glass)", op=0.55)
    c.rect(MOD_W-0.35, 0.35, 0.35, 0.62, "var(--desk)")
    c.rect(MOD_W, 0, TAB, ALT, "var(--wall)")
    c.rect(X0, 0.35, 0.35, 0.62, "var(--desk)")
    c.rect(ANCHO-0.55, 0.46, 0.55, 0.30, "#585650")
    c.rect(ANCHO-0.55, 0.76, 0.55, 0.05, "#6b6862")
    c.rect(ANCHO-0.02, 0.90, 0.02, 0.95, "var(--glass)", op=0.55)
    c.rect(ANCHO, 0, 0.15, ALT, "var(--wall)")
    franja_abierta(c, -0.15, ANCHO+0.15)

    # cotas de altura, todas al lado izquierdo en columna para no chocar
    c.cota_v(-0.34, 0, ALT, "2,80 muro")
    c.cota_v(ANCHO+0.20, 0.46, 0.81, "0,80 mesón")
    c.cota_v(ANCHO+0.20, 0.90, 1.85, "espejo")
    c.cota_v(-0.34, 0.35, 0.97, "0,62 urinario")
    c.cota_h(0, ANCHO, ALT+0.30, "9,83 m — ancho libre entre muros")

    # títulos, en su propia franja arriba, bien separados
    c.texto(ANCHO/2, ALT+0.62, "SIN TECHO PROPIO — ABIERTO A LA CUBIERTA DEL GALPÓN", "mb")
    c.texto(ANCHO/2, ALT+0.92, "CORTE A-A — TRANSVERSAL, a y=3,00 m (por urinarios y mesones)", "ct", fill="var(--ink)")

    # leyenda en una fila al pie
    c.texto(0.28, -0.20, "MESÓN A", "mb")
    c.texto(MOD_W-0.17, -0.20, "URIN. A", "mb")
    c.texto(X0+0.17, -0.35, "URIN. B", "mb")
    c.texto(ANCHO-0.28, -0.20, "MESÓN B", "mb")
    return c.cerrar("Corte A-A transversal")


# ============================================================ CORTE B-B (longitudinal, x=X0+1.35, módulo B)
def corte_BB():
    c = Corte(-1.3, FONDO+1.3)
    c.rect(-0.5, -0.05, FONDO+1.0, 0.05, "var(--floor)", "none")
    c.linea(-0.5, 0, 4.75, 0, "var(--wall)", 2)
    c.linea(4.75, 0, 4.85, -0.025, "var(--wall)", 2)
    c.linea(4.85, -0.025, FONDO+0.5, 0, "var(--wall)", 2)
    c.rect(-0.15, 0, 0.15, ALT, "var(--wall)")
    c.rect(0, 0, 1.50, 1.80, "var(--desk)", "var(--deskLn)", op=0.35)
    c.linea(1.50, 0, 1.50, 1.80, "var(--ink)", 2.2)
    c.rect(FONDO, 0, 0.15, ALT, "var(--wall)")
    franja_abierta(c, -0.15, FONDO+0.15)

    c.cota_v(-0.34, 0, ALT, "2,80 muro")
    c.cota_v(1.66, 0, 1.80, "1,80 partición")
    c.cota_h(0, FONDO, ALT+0.30, "5,00 m — fondo")

    c.texto(FONDO/2, ALT+0.62, "SIN TECHO PROPIO — ABIERTO A LA CUBIERTA DEL GALPÓN", "mb")
    c.texto(FONDO/2, ALT+0.92, "CORTE B-B — LONGITUDINAL (cubículo + rejilla)", "ct", fill="var(--ink)")

    c.texto(0.75, -0.20, "CUBÍCULO · FENÓLICO", "mb")
    c.texto(4.85, -0.20, "REJILLA · pendiente 1,5–2 %", "mb")
    return c.cerrar("Corte B-B longitudinal")


# ============================================================ CORTE C-C (transversal, y=0.75, por cubículos)
def corte_CC():
    c = Corte(-0.5, ANCHO+1.5)
    c.rect(-0.5, -0.05, ANCHO+1.0, 0.05, "var(--floor)", "none")
    c.linea(-0.5, 0, ANCHO+0.5, 0, "var(--wall)", 2)
    c.rect(-0.15, 0, 0.15, ALT, "var(--wall)")
    # fila de cubículos A: x MOD_W-2.70 .. MOD_W
    xa = MOD_W - 2.70
    c.rect(xa, 0, 2.70, 1.80, "var(--desk)", "var(--deskLn)", op=0.35)
    for k in range(1, 3):
        c.linea(xa+k*0.90, 0, xa+k*0.90, 1.80, "var(--deskLn)", 1)
    c.rect(MOD_W, 0, TAB, ALT, "var(--wall)")
    # fila de cubículos B: x X0 .. X0+2.70
    c.rect(X0, 0, 2.70, 1.80, "var(--desk)", "var(--deskLn)", op=0.35)
    for k in range(1, 3):
        c.linea(X0+k*0.90, 0, X0+k*0.90, 1.80, "var(--deskLn)", 1)
    c.rect(ANCHO, 0, 0.15, ALT, "var(--wall)")
    franja_abierta(c, -0.15, ANCHO+0.15)

    c.cota_v(-0.34, 0, ALT, "2,80 muro")
    c.cota_v(ANCHO+0.20, 0, 1.80, "1,80 partición")
    c.cota_h(0, ANCHO, ALT+0.30, "9,83 m — ancho libre entre muros")
    c.texto(ANCHO/2, ALT+0.62, "SIN TECHO PROPIO — ABIERTO A LA CUBIERTA DEL GALPÓN", "mb")
    c.texto(ANCHO/2, ALT+0.92, "CORTE C-C — TRANSVERSAL, a y=0,75 m (por cubículos)", "ct", fill="var(--ink)")
    c.texto(xa+1.35, -0.20, "CUBÍCULOS A", "mb")
    c.texto(X0+1.35, -0.20, "CUBÍCULOS B", "mb")
    return c.cerrar("Corte C-C transversal por cubículos")


# ============================================================ ELEVACIONES INTERIORES (vista frontal de una pared, de pie dentro del baño)
def elev_urinarios():
    """Pared del tabique vista de frente desde dentro del módulo B: los 4 urinarios en fila."""
    largo = 3.00
    pad = 2.0
    c = Corte(-pad, largo+pad, z_lo=-0.55, z_hi=ALT+1.05)
    c.rect(-pad, -0.05, largo+2*pad, 0.05, "var(--floor)", "none")
    c.linea(-pad, 0, largo+pad, 0, "var(--wall)", 2)
    c.rect(-pad, 0, largo+2*pad, ALT, "var(--wall)", op=0.30)   # paño del tabique, de fondo
    paso, pieza = 0.75, 0.60
    for k in range(4):
        x0k = paso*k + (paso-pieza)/2
        c.rect(x0k, 0.35, pieza, 0.62, "var(--desk)", "var(--ink)", sw=1.6)
        c.linea(x0k+pieza/2, 0.97, x0k+pieza/2, 1.15, "var(--dim)", 1.4)  # tubo fluxómetro
    franja_abierta(c, -pad, largo+pad)
    c.cota_v(-0.42, 0.35, 0.97, "0,62")
    c.cota_h(0.075, largo-0.075, ALT+0.30, "3,00 m — 4 urinarios a 0,75 m")
    c.texto(largo/2, ALT+0.62, "SIN TECHO PROPIO", "mb")
    c.texto(largo/2, ALT+0.92, "ELEVACIÓN E-E — PARED DE URINARIOS", "ct", fill="var(--ink)")
    return c.cerrar("Elevación interior pared de urinarios")


def elev_meson():
    """Mesón de lavamanos + espejo, vista de frente desde dentro del módulo."""
    largo = 2.40
    pad = 2.0
    c = Corte(-pad, largo+pad, z_lo=-0.55, z_hi=ALT+1.05)
    c.rect(-pad, -0.05, largo+2*pad, 0.05, "var(--floor)", "none")
    c.linea(-pad, 0, largo+pad, 0, "var(--wall)", 2)
    c.rect(-pad, 0, largo+2*pad, ALT, "var(--wall)", op=0.30)
    c.rect(0, 0.46, largo, 0.30, "#585650")
    c.rect(0, 0.76, largo, 0.05, "#6b6862")
    for k in range(3):
        cx = largo*(k+0.5)/3
        c.o.append(f'<ellipse cx="{c.X(cx):.1f}" cy="{c.Z(0.81):.1f}" rx="14" ry="6" '
                    f'fill="var(--floor)" stroke="var(--ink)" stroke-width="1"/>')
    c.rect(0.06, 0.90, largo-0.12, 0.95, "var(--glass)", op=0.55)
    franja_abierta(c, -pad, largo+pad)
    c.cota_v(-0.42, 0.46, 0.81, "0,80 mesón")
    c.cota_v(largo+0.20, 0.90, 1.85, "espejo")
    c.cota_h(0, largo, ALT+0.30, "2,40 m — 3 lavamanos a 0,80 m")
    c.texto(largo/2, ALT+0.62, "SIN TECHO PROPIO", "mb")
    c.texto(largo/2, ALT+0.92, "ELEVACIÓN F-F — PARED DEL MESÓN", "ct", fill="var(--ink)")
    return c.cerrar("Elevación interior pared del mesón")


def elev_cubiculos():
    """Fila de 3 puertas de cubículo, vista de frente desde dentro del módulo."""
    largo = 2.70
    pad = 2.0
    c = Corte(-pad, largo+pad, z_lo=-0.55, z_hi=ALT+1.05)
    c.rect(-pad, -0.05, largo+2*pad, 0.05, "var(--floor)", "none")
    c.linea(-pad, 0, largo+pad, 0, "var(--wall)", 2)
    c.rect(-pad, 0, largo+2*pad, ALT, "var(--wall)", op=0.14)
    c.rect(0, 0, largo, 1.80, "var(--desk)", "var(--deskLn)", op=0.7)
    for k in range(1, 3):
        c.linea(k*0.90, 0, k*0.90, 1.80, "var(--ink)", 2)
    for k in range(3):
        cx = k*0.90 + 0.45
        c.rect(cx-0.37, 0.02, 0.74, 1.55, "var(--ink)", "none", op=0.88)
        c.texto(cx, -0.20, f"C{k+1}", "mb")
    franja_abierta(c, -pad, largo+pad)
    c.cota_v(-0.42, 0, 1.80, "1,80 partición")
    c.cota_h(0, largo, ALT+0.30, "2,70 m — 3 cubículos de 0,90 m")
    c.texto(largo/2, ALT+0.62, "SIN TECHO PROPIO", "mb")
    c.texto(largo/2, ALT+0.92, "ELEVACIÓN G-G — PUERTAS DE CUBÍCULOS", "ct", fill="var(--ink)")
    return c.cerrar("Elevación interior puertas de cubículos")


if __name__ == "__main__":
    out = "/tmp/claude-0/-home-user-produccion-studio/344e1d7f-bb05-50a6-8219-29e2715272fc/scratchpad"
    open(f"{out}/corte_AA.svg", "w").write(corte_AA())
    open(f"{out}/corte_BB.svg", "w").write(corte_BB())
    open(f"{out}/corte_CC.svg", "w").write(corte_CC())
    open(f"{out}/elev_urinarios.svg", "w").write(elev_urinarios())
    open(f"{out}/elev_meson.svg", "w").write(elev_meson())
    open(f"{out}/elev_cubiculos.svg", "w").write(elev_cubiculos())
    print("cortes y elevaciones generados")
