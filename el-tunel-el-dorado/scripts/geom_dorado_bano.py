# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "/root/.claude/skills/synced/b15c0002-62bd-40fe-a19e-7a44ad7aab64_5609b3a6-1141-4780-91d5-d1402400a469/plano-tecnico/scripts")
from planta import Planta, area_poligono, perimetro

ANCHO = 9.83   # corregido: medida real confirmada (no 9,50 m)
FONDO = 5.00
TAB = 0.15

contorno = [(0,0),(ANCHO,0),(ANCHO,FONDO),(0,FONDO)]
p = Planta(contorno, area_declarada=ANCHO*FONDO)
MOD_W = (ANCHO - TAB) / 2
X0 = MOD_W + TAB
print("Ancho por módulo:", MOD_W, " | inicio módulo B (derecha):", X0)
print("Área bruta:", ANCHO*FONDO)

zonas = [
    {"n":"Tabique", "r":(MOD_W, 0, TAB, FONDO)},

    # HOMBRES A (izquierda) — pegado al tabique
    {"n":"Cubículo A1", "r":(MOD_W-2.70, 0, 0.90, 1.50)},
    {"n":"Cubículo A2", "r":(MOD_W-1.80, 0, 0.90, 1.50)},
    {"n":"Cubículo A3 (pegado al tabique)", "r":(MOD_W-0.90, 0, 0.90, 1.50)},
    {"n":"Urinarios A ×4 (paño tabique)", "r":(MOD_W-0.35, 1.70, 0.35, 3.00)},
    {"n":"Mesón lavamanos A", "r":(0, 1.30, 0.55, 2.40)},
    {"n":"Banco de sillas A (esquina liberada)", "r":(0.20, 0, 1.60, 0.45)},
    {"n":"Puerta A (barrido, extremo izq.)", "r":(0.20, 4.55, 0.90, 0.45)},

    # HOMBRES B (derecha) — pegado al tabique
    {"n":"Cubículo B1 (pegado al tabique)", "r":(X0, 0, 0.90, 1.50)},
    {"n":"Cubículo B2", "r":(X0+0.90, 0, 0.90, 1.50)},
    {"n":"Cubículo B3", "r":(X0+1.80, 0, 0.90, 1.50)},
    {"n":"Urinarios B ×4 (paño tabique)", "r":(X0, 1.70, 0.35, 3.00)},
    {"n":"Mesón lavamanos B", "r":(ANCHO-0.55, 1.30, 0.55, 2.40)},
    {"n":"Banco de sillas B (esquina liberada)", "r":(ANCHO-1.80, 0, 1.60, 0.45)},
    {"n":"Puerta B (barrido, extremo der.)", "r":(ANCHO-1.10, 4.55, 0.90, 0.45)},
]

res = p.verificar(zonas)
for z in res:
    print(f"{z['n']:<38} r={z['r']}  area={z['a']:.2f} m²")

print("\nOK: verificado por shapely — ninguna zona sale del contorno ni se solapa.")
print("Total piezas: 6 pocetas + 8 urinarios + 6 lavamanos = 20 piezas, 2 bancos, 2 puertas.")
