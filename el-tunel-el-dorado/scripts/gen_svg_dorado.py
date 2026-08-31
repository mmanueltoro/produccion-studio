# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/root/.claude/skills/synced/b15c0002-62bd-40fe-a19e-7a44ad7aab64_5609b3a6-1141-4780-91d5-d1402400a469/plano-tecnico/scripts")
from planta import Lienzo

ANCHO, FONDO, TAB = 9.83, 5.00, 0.15   # ANCHO corregido a la medida real confirmada
MOD_W = (ANCHO - TAB) / 2   # 4.84
X0 = MOD_W + TAB            # inicio módulo B (derecha) = 4.99

L = Lienzo(ANCHO, FONDO, escala=64, margen=56)
L.abrir("Planta módulo sanitario El Túnel — 9,83 x 5,00 m, dos baños de hombres")
contorno = [(0,0),(ANCHO,0),(ANCHO,FONDO),(0,FONDO)]
L.suelo(contorno)

def rectp(x,y,w,h,fill,stroke=None,op=1,extra=""):
    X,Y,M=L.X,L.Y,L.M
    s = f' stroke="{stroke}" stroke-width="1.4"' if stroke else ""
    L.o.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*M:.1f}" height="{h*M:.1f}" '
                f'fill="{fill}" fill-opacity="{op}"{s} {extra}/>')

def linep(x1,y1,x2,y2,stroke,w=1.2,dash=""):
    X,Y=L.X,L.Y
    d = f' stroke-dasharray="{dash}"' if dash else ""
    L.o.append(f'<line x1="{X(x1):.1f}" y1="{Y(y1):.1f}" x2="{X(x2):.1f}" y2="{Y(y2):.1f}" '
                f'stroke="{stroke}" stroke-width="{w}"{d}/>')

def circp(cx,cy,r,fill="none",stroke="var(--deskLn)",w=1.2):
    X,Y,M=L.X,L.Y,L.M
    L.o.append(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{r*M:.1f}" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="{w}"/>')

def cubiculo(x,y,w,h,label):
    rectp(x,y,w,h,"none","var(--deskLn)")
    linep(x,y,x,y+h,"var(--deskLn)",1)
    linep(x+w,y,x+w,y+h,"var(--deskLn)",1)
    bw,bh = w*0.62, h*0.36
    bx,by = x+(w-bw)/2, y+h*0.18
    rectp(bx,by,bw,bh*0.30,"var(--desk)","var(--deskLn)")
    circp(x+w/2, by+bh*0.30+bh*0.55, bw*0.30, "var(--desk)", "var(--deskLn)")
    L.puerta(x, y+h, ancho=w*0.9, gozne="izq", hacia="arriba")
    L.o.append(f'<text x="{L.X(x+w/2):.1f}" y="{L.Y(y+h*0.09):.1f}" text-anchor="middle" '
                f'class="mb" fill="var(--muted)">{label}</text>')

def urinario(x,y,w,h,n):
    rectp(x,y,w,h,"var(--desk)","var(--deskLn)",0.9)
    paso = h/n
    for k in range(n):
        cy = y + paso*(k+0.5)
        circp(x+w*0.55, cy, w*0.34, "var(--surface)", "var(--deskLn)")
        linep(x, cy-0.02, x, cy+0.02, "var(--wall)", 3)

def meson(x,y,w,h,n):
    rectp(x,y,w,h,"var(--desk)","var(--deskLn)")
    paso = h/n
    for k in range(n):
        cy = y + paso*(k+0.5)
        circp(x+w*0.5, cy, min(w,paso)*0.30, "var(--surface)", "var(--deskLn)")
    linep(x-0.02, y, x-0.02, y+h, "var(--glass)", 3)

def meson_der(x,y,w,h,n):
    rectp(x,y,w,h,"var(--desk)","var(--deskLn)")
    paso = h/n
    for k in range(n):
        cy = y + paso*(k+0.5)
        circp(x+w*0.5, cy, min(w,paso)*0.30, "var(--surface)", "var(--deskLn)")
    linep(x+w+0.02, y, x+w+0.02, y+h, "var(--glass)", 3)

def banco(x,y,w,h,n=4):
    rectp(x,y,w,h,"var(--cafebar)","var(--deskLn)",0.55)
    paso = w/n
    for k in range(n):
        cx = x + paso*(k+0.5)
        circp(cx, y+h*0.5, min(h,paso)*0.34, "none", "var(--deskLn)")
    L.o.append(f'<text x="{L.X(x+w/2):.1f}" y="{L.Y(y+h)+11:.1f}" text-anchor="middle" '
                f'class="mb" fill="var(--muted)">BANCO</text>')

# ---------------- HOMBRES A (izquierda) — pegado al tabique ----------------
for i,cx in enumerate([MOD_W-2.70, MOD_W-1.80, MOD_W-0.90]):
    cubiculo(cx, 0, 0.90, 1.50, f"A{i+1}")
urinario(MOD_W-0.35, 1.70, 0.35, 3.00, 4)
meson(0, 1.30, 0.55, 2.40, 3)
banco(0.20, 0, 1.60, 0.45)
L.puerta(0.20, FONDO, ancho=0.90, gozne="izq", hacia="arriba")

# ---------------- HOMBRES B (derecha) — pegado al tabique ----------------
for i,cx in enumerate([X0, X0+0.90, X0+1.80]):
    cubiculo(cx, 0, 0.90, 1.50, f"B{i+1}")
urinario(X0, 1.70, 0.35, 3.00, 4)
meson_der(ANCHO-0.55, 1.30, 0.55, 2.40, 3)
banco(ANCHO-1.80, 0, 1.60, 0.45)
L.puerta(ANCHO-1.10, FONDO, ancho=0.90, gozne="der", hacia="arriba")

# ---------------- Rejillas de piso (descarga) ----------------
circp(MOD_W-1.35, 4.85, 0.09, "none", "var(--accent)", 1.4)
circp(X0+1.35, 4.85, 0.09, "none", "var(--accent)", 1.4)

# ---------------- Tabique central ----------------
rectp(MOD_W, 0, TAB, FONDO, "var(--wall)", None, 1)

# ---------------- Muros perimetrales ----------------
L.muros()

# ---------------- Cotas ----------------
top = L.Y(0) - 34
L.cota(L.X(0), top, L.X(ANCHO), top, "9,83 m — ancho libre entre muros")
L.cota(L.X(0), top+16, L.X(MOD_W), top+16, "4,84 m")
L.cota(L.X(X0), top+16, L.X(ANCHO), top+16, "4,84 m")
left = L.X(0) - 26
L.cota(left, L.Y(0), left, L.Y(FONDO), "5,00 m — fondo", vertical=True)
L.cota(L.X(MOD_W), L.Y(FONDO)+18, L.X(X0), L.Y(FONDO)+18, "0,15")
L.cota(L.X(MOD_W-2.70), L.Y(1.50)+16, L.X(MOD_W), L.Y(1.50)+16, "3 × 0,90 = 2,70 m")
L.cota(L.X(X0), L.Y(1.50)+16, L.X(X0+2.70), L.Y(1.50)+16, "3 × 0,90 = 2,70 m")
L.cota(L.X(MOD_W-0.35)-10, L.Y(1.70), L.X(MOD_W-0.35)-10, L.Y(4.70), "4 × 0,75 = 3,00 m", vertical=True)
L.cota(L.X(X0+0.35)+10, L.Y(1.70), L.X(X0+0.35)+10, L.Y(4.70), "4 × 0,75 = 3,00 m", vertical=True)

L.o.append(f'<text x="{L.X(MOD_W/2):.1f}" y="{L.Y(4.55)-6:.1f}" text-anchor="middle" class="zl" fill="var(--ink)">BAÑO DE HOMBRES A</text>')
L.o.append(f'<text x="{L.X(X0+MOD_W/2):.1f}" y="{L.Y(4.55)-6:.1f}" text-anchor="middle" class="zl" fill="var(--ink)">BAÑO DE HOMBRES B</text>')

svg = L.cerrar()
open("/tmp/claude-0/-home-user-produccion-studio/344e1d7f-bb05-50a6-8219-29e2715272fc/scratchpad/plano_dorado.svg","w").write(svg)
print("SVG generado,", len(svg), "chars")
