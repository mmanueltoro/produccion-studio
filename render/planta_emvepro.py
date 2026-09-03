# -*- coding: utf-8 -*-
"""
Planta del caso piloto VP Emvepro: contorno con cotas, obstáculos, zonas cerradas
y mobiliario empacado. Produce planta.pkl para modelo3d.py.

Uso:  python3 render/planta_emvepro.py [salida.pkl]
"""
import sys, os, pickle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from planta import Planta, empacar, area_poligono

# Contorno en metros (origen esquina noroeste, x este, y sur). Mismo que modelo3d.py.
CONT = [(0, 0), (12.35, 0), (12.35, 1.60), (14.56, 1.60), (14.56, 9.41), (11.51, 9.41),
        (11.51, 8.87), (8.14, 8.87), (8.14, 8.24), (3.22, 8.24), (3.22, 7.08), (0, 7.08)]
COLUMNA = (2.60, 0.85, 1.45, 1.60)          # x, y, ancho, fondo
VENTANAL = [(3.32, 12.35, 0.0)]             # tramo de vidrio en la fachada norte

p = Planta(CONT, obstaculos=[COLUMNA], ventanales=VENTANAL)
print(f"área bruta {p.area_bruta:.2f} m² · útil {p.area_util:.2f} m² "
      f"(zapatero {area_poligono(CONT):.2f})")

# Zonas cerradas. El orden importa: modelo3d.py toma Z[1] como la sala de reuniones.
ZONAS = [
    dict(n="Cuarto de redes",   k="redes",   r=(0.00, 0.00, 3.32, 3.60)),
    dict(n="Sala de reuniones", k="reunion", r=(9.06, 1.60, 5.50, 3.30)),
    dict(n="Oficina privada",   k="pecera",  r=(11.51, 4.90, 3.05, 4.51)),
]
p.verificar(ZONAS)
for z in ZONAS:
    print(f"  {z['n']:<18} {z['a']:6.2f} m²")

# Superficies que el empacador no puede usar: barrido de puertas, corredor de acceso
# y el mobiliario fijo que modelo3d.py coloca (impresión, café, barras de muro).
EXCLUIR = [
    (0.20, 3.60, 1.10, 1.10),   # puerta del cuarto de redes
    (5.30, 6.70, 1.50, 1.54),   # acceso principal (fachada sur) y su corredor
    (1.20, 3.70, 1.85, 0.85),   # mueble de impresión
    (0.20, 6.30, 2.90, 0.78),   # punto de café + lámpara de pie
    (3.40, 7.20, 1.90, 1.04),   # barra de muro 2 pax
    (8.20, 7.50, 2.60, 1.37),   # barra de muro 3 pax
    (9.06, 0.00, 3.29, 1.60),   # corredor frente al ventanal, junto a la sala
]
libre = p.abierta(ZONAS, excluir=EXCLUIR)
print(f"área abierta disponible {libre.area:.2f} m²")

MESAS = empacar(libre)
plazas = sum(m["pl"] for m in MESAS)
vent, tramos = p.ventanal_libre(ZONAS)
print(f"mobiliario: {len(MESAS)} módulos · {plazas} plazas en área abierta")
print(f"ventanal libre {vent:.2f} m en {len(tramos)} tramo(s)")
for m in MESAS:
    print(f"  mesa {m['pl']}pax en ({m['x']:.2f},{m['y']:.2f}) {'vertical' if m['rot'] else 'horizontal'}")

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "salida", "planta.pkl")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
pickle.dump(dict(CONT=CONT, ZONAS=ZONAS, MESAS=MESAS, PLAZAS=plazas), open(OUT, "wb"))
print("->", OUT)
