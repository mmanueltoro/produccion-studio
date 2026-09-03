# -*- coding: utf-8 -*-
"""
Lanza el render con Blender como módulo de Python (pip install bpy==4.2.*),
sin necesidad del ejecutable `blender`. Mismos argumentos que render_blender.py:

    python3 render/render.py VISTA SAMPLES ANCHO ALTO SALIDA.png
    python3 render/render.py A 56 1000 640 render/salida/vista_A.png

Con el ejecutable oficial de Blender el equivalente es:
    MODELO_OBJ=render/salida/modelo.obj blender -b -P render/scripts/render_blender.py -- A 56 1000 640 salida.png
"""
import os, sys, runpy, time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MODELO_OBJ", os.path.join(AQUI, "salida", "modelo.obj"))
os.environ.setdefault("HDRI", os.path.join(AQUI, "cielo.hdr"))

args = sys.argv[1:] or ["A"]
if len(args) < 5:
    vista = args[0]
    args = [vista, *(args[1:] + ["56", "1000", "640"][len(args)-1:]),
            os.path.join(AQUI, "salida", f"vista_{vista}.png")][:5]
sys.argv = ["blender", "--", *args]

t0 = time.time()
runpy.run_path(os.path.join(AQUI, "scripts", "render_blender.py"), run_name="__main__")
print(f"tiempo total {time.time()-t0:.0f} s")
