# -*- coding: utf-8 -*-
"""Modelo 3D a escala real del módulo sanitario "El Túnel" (proyecto El Dorado),
generado desde las mismas coordenadas verificadas del plano (no a ojo).
Ejes: X este (ancho), Y arriba (altura), Z sur (fondo). Unidades: metros.
Abrir directo en SketchUp / Fusion / Blender (importar OBJ)."""

ANCHO, FONDO, TAB = 9.83, 5.00, 0.15
MOD_W = (ANCHO - TAB) / 2   # 4.84
X0 = MOD_W + TAB            # 4.99
ALT = 2.80

V, F, G = [], [], []

def box3(x, y, z, w, h, dp, name):
    """Caja con origen en la esquina inferior (x,y,z), ancho w (X), alto h (Y), fondo dp (Z)."""
    i = len(V) + 1
    for (dx, dy, dz) in [(0,0,0),(w,0,0),(w,0,dp),(0,0,dp),(0,h,0),(w,h,0),(w,h,dp),(0,h,dp)]:
        V.append((x+dx, y+dy, z+dz))
    G.append((name, len(F)))
    for a in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        F.append(tuple(i+k for k in a))

def cyl(cx, y, cz, r, h, name, seg=14):
    import math
    i = len(V) + 1
    for yy in (y, y+h):
        for k in range(seg):
            a = 2*math.pi*k/seg
            V.append((cx+r*math.cos(a), yy, cz+r*math.sin(a)))
    G.append((name, len(F)))
    for k in range(seg):
        k2 = (k+1) % seg
        F.append((i+k, i+k2, i+seg+k2, i+seg+k))
    F.append(tuple(i+k for k in range(seg)))
    F.append(tuple(i+seg+k for k in range(seg-1,-1,-1)))

# ---------------- piso ----------------
box3(0, -0.03, 0, ANCHO, 0.03, FONDO, "PISO_epoxico_gris_cemento")

# ---------------- muros ----------------
box3(-0.15, 0, -0.15, ANCHO+0.30, ALT, 0.15, "muro_trasero")           # trasero (existente)
box3(-0.15, 0, -0.15, 0.15, ALT, FONDO+0.30, "muro_lateral_izq")       # existente
box3(ANCHO, 0, -0.15, 0.15, ALT, FONDO+0.30, "muro_lateral_der")       # existente
box3(MOD_W, 0, 0, TAB, ALT, FONDO, "tabique_central")                  # nuevo

def cubiculos(x0, n, prefix):
    for k in range(n):
        cx = x0 + k*0.90
        if k > 0:
            box3(cx-0.01, 0, 0, 0.02, 1.80, 1.50, f"tabiqueria_fenolico_{prefix}")
        # inodoro esquemático: base + tanque
        box3(cx+0.20, 0, 0.05, 0.50, 0.34, 0.14, f"inodoro_tanque_{prefix}{k+1}")
        cyl(cx+0.45, 0, 0.55, 0.28, 0.40, f"inodoro_taza_{prefix}{k+1}")
    # panel divisorio final + puerta por unidad
    box3(x0-0.01, 0, 0, 0.02, 1.80, 1.50, f"tabiqueria_fenolico_{prefix}")
    box3(x0+n*0.90-0.01, 0, 0, 0.02, 1.80, 1.50, f"tabiqueria_fenolico_{prefix}")
    for k in range(n):
        cx = x0 + k*0.90
        box3(cx+0.08, 0, 1.49, 0.74, 1.55, 0.02, f"PUERTA_CUBICULO_{prefix}{k+1}")

def urinarios(x_tab, n, hacia_der):
    paso, pieza = 0.75, 0.60
    ux = x_tab if not hacia_der else x_tab - 0.32
    for k in range(n):
        z0 = 1.70 + paso*k + (paso-pieza)/2
        box3(ux, 0.35, z0, 0.32, 0.62, pieza, f"urinario_{k+1}")
        cyl(ux+0.16 if not hacia_der else ux+0.16, 0.62, z0+pieza/2, 0.03, 0.35, f"tuberia_fluxometro_{k+1}", 8)

def meson(x, hacia_der, n, largo):
    w = 0.55
    xx = x if not hacia_der else x - w
    box3(xx, 0.46, 1.30, w, 0.30, largo, "meson_frente_concreto")       # apron
    box3(xx, 0.76, 1.30, w, 0.05, largo, "meson_tope_concreto")         # tope
    for k in range(n):
        cz = 1.30 + largo*(k+0.5)/n
        cyl(xx+w*0.5, 0.81, cz, 0.16, 0.03, f"lavamanos_{k+1}", 16)
        cyl(xx+w*0.5, 0.81, cz, 0.012, 0.18, f"griferia_{k+1}", 8)
    mx = x if not hacia_der else x-0.02
    box3(mx, 0.90, 1.30, 0.02, 0.95, largo, "espejo")

def banco(x, z, w, dp):
    box3(x, 0.42, z, w, 0.05, dp, "banco_asiento")
    for lx in (x+0.08, x+w-0.08-0.05):
        for lz in (z+0.05, z+dp-0.05-0.05):
            box3(lx, 0, lz, 0.05, 0.42, 0.05, "banco_pata_metal")

def puerta_acceso(x, w):
    box3(x, 0, FONDO-0.02, w, 2.10, 0.04, "PUERTA_ACCESO_negro_mate")

# ---------------- MÓDULO A (izquierda) ----------------
cubiculos(MOD_W-2.70, 3, "A")
urinarios(MOD_W, 4, hacia_der=True)
meson(0, False, 3, 2.40)
banco(0.20, 0, 1.60, 0.45)
puerta_acceso(0.20, 0.90)

# ---------------- MÓDULO B (derecha) ----------------
cubiculos(X0, 3, "B")
urinarios(X0, 4, hacia_der=False)
meson(ANCHO, True, 3, 2.40)
banco(ANCHO-1.80, 0, 1.60, 0.45)
puerta_acceso(ANCHO-1.10, 0.90)

# ---------------- export OBJ ----------------
lines = [
    "# Módulo sanitario El Túnel - proyecto El Dorado",
    "# Modelo 3D a escala real, en metros. Ejes: X este, Y arriba, Z sur.",
    "# Ancho libre 9,83 m x Fondo 5,00 m, tabique 0,15 m, altura de muro 2,80 m.",
    "# Sin techo propio (abierto a la cubierta del galpon) - no se modela cielorraso.",
    "# Generado desde las coordenadas verificadas del plano (shapely, sin solapes).",
]
for (x, y, z) in V:
    lines.append(f"v {x:.4f} {y:.4f} {z:.4f}")
gi = 0
for i, f in enumerate(F):
    while gi < len(G) and G[gi][1] == i:
        lines.append(f"g {G[gi][0]}")
        gi += 1
    lines.append("f " + " ".join(str(k) for k in f))

out_path = "/tmp/claude-0/-home-user-produccion-studio/344e1d7f-bb05-50a6-8219-29e2715272fc/scratchpad/modulo_sanitario_el_tunel.obj"
open(out_path, "w").write("\n".join(lines) + "\n")
print(f"OBJ: {len(V)} vertices, {len(F)} caras, {len(set(g[0] for g in G))} objetos nombrados")
print("Guardado en:", out_path)
