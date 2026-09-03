# Render calculado · MundoXpress

Pipeline **planta → modelo 3D → render Cycles** del caso piloto VP Emvepro
(116.07 m² útiles, altura libre 2.70 m). Las medidas se calculan, no se aproximan:
la planta pasa `verificar()` antes de levantar el modelo, y el render parte de esa
geometría real.

    cotas -> planta_emvepro.py -> salida/planta.pkl
          -> scripts/modelo3d.py -> salida/modelo.obj  (52 objetos nombrados)
          -> render.py (bpy)  ó  blender -b -P scripts/render_blender.py -> salida/vista_*.png

## Requisitos

```bash
pip install shapely qrcode "bpy==4.2.*"     # bpy = Blender como módulo de Python (3.11)
```

`bpy` incluye Cycles y el denoiser OpenImageDenoise, así que no hace falta el
ejecutable de Blender. Si ya tienes Blender 4.2 instalado, `scripts/render_blender.py`
se lanza igual con `blender -b -P` (ver abajo).

## Uso

```bash
python3 render/planta_emvepro.py                                   # verifica y empaca
python3 render/scripts/modelo3d.py render/salida/planta.pkl render/salida/modelo.obj
python3 render/render.py A 64 1200 768 render/salida/vista_A.png   # vista samples ancho alto salida
python3 render/render.py B 64 1200 768 render/salida/vista_B.png
python3 render/render.py cenital 64 1200 768 render/salida/vista_cenital.png
```

Con el ejecutable oficial:

```bash
MODELO_OBJ=render/salida/modelo.obj HDRI=render/cielo.hdr \
  blender -b -P render/scripts/render_blender.py -- A 64 1200 768 render/salida/vista_A.png
```

**HDRI.** Si existe `render/cielo.hdr` (Poly Haven, CC0) se usa como cielo. Si no,
el script arma un cielo físico Nishita alineado con el sol de la escena.

```bash
curl -sL -o render/cielo.hdr https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/kloofendal_48d_partly_cloudy_puresky_2k.hdr
```

**Tiempos medidos** (4 núcleos, bpy 4.2.23, cielo procedural): 1200×768 a 64 muestras
con denoiser ≈ 30–40 s por vista. Escala casi lineal con píxeles y muestras.

## Exportar a D5 / Twinmotion

D5 Render no lee OBJ. Con `assimp` instalado: `assimp export salida/modelo.obj modelo.fbx`.
Los nombres de objeto (`mesa_8pax`, `vidrio_ventanal`, `SILLA`…) sobreviven la
conversión y permiten asignar materiales uno por uno del otro lado.

## Resultado del piloto (planta_emvepro.py)

| Zona | m² |
|---|---|
| Área útil (bruta 118.39 − columna) | 116.07 |
| Cuarto de redes | 10.80 |
| Sala de reuniones | 18.15 |
| Oficina privada | 13.76 |
| Área abierta disponible | 55.30 |

Mobiliario empacado en área abierta: 4 módulos, **23 plazas**; ventanal libre 9.03 m en un
solo tramo. La sala de reuniones suma 10 y la oficina privada 3.
