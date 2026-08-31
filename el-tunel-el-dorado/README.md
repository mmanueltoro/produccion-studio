# Módulo sanitario "El Túnel" — Proyecto El Dorado

Estado al 31/08: plano técnico verificado + cotización + modelo 3D. Pendiente: acabados finales por confirmar y decidir vía de render (ver abajo).

## Datos verificados del local
- Ancho libre entre muros: **9,83 m** (confirmado por el cliente; coincide con el levantamiento del visor 360° "El Túnel")
- Fondo: **5,00 m**
- Tabique central: **0,15 m** → dos módulos de **4,84 m** cada uno
- Altura de muro: **2,80 m**, sin techo propio (abierto a la cubierta del galpón)
- Área bruta: **49,15 m²**

## Distribución (verificada por cálculo, shapely, sin solapes)
Dos baños de hombres idénticos y espejados (A izquierda, B derecha), separados por el tabique:
- 3 pocetas por lado (0,90 × 1,50 m c/u), pegadas al tabique
- 4 urinarios por lado (0,75 m a eje, 3,00 m corrido, contra el paño del tabique)
- 3 lavamanos por lado (mesón corrido de 2,40 m en concreto pulido, contra el muro exterior)
- Espejo corrido sobre cada mesón
- Banco de sillas (1,60 × 0,45 m) en la esquina liberada junto a cada mesón
- Puertas de acceso en los extremos opuestos del frente (izquierda y derecha, no al centro)
- **Total: 20 piezas sanitarias** (6 pocetas + 8 urinarios + 6 lavamanos)

## Acabados — minimalista industrial
Piso en pintura epóxica gris cemento (con desagüe y pendiente 1,5–2%), paredes en
microcemento gris claro, mesón y frente en concreto pulido, tabiquería de cubículos en
fenólico gris oscuro, herrajes y grifería en negro mate / acero inoxidable.

## Archivos de este proyecto
- `plano_el_dorado.html` — plano técnico completo (cajetín, veredicto, cómputo de piezas,
  acabados, lista de materiales, 6 cortes/elevaciones con sus prompts de IA). También
  publicado como Artifact: https://claude.ai/code/artifact/07c88cae-a206-4610-8fd6-9ac744211936
- `El_Tunel_cotizacion_materiales.xlsx` — lista de materiales con columna de precio
  unitario/total, lista para armar la cotización.
- `modulo_sanitario_el_tunel.obj` — modelo 3D a escala real (992 vértices, 45 objetos
  nombrados). Abrir en SketchUp / Fusion 360 / Blender.
- `scripts/` — generadores en Python de todo lo anterior (geometría verificada con
  shapely, SVG del plano, cortes/elevaciones, modelo 3D, xlsx). Reejecutables si cambian
  las medidas.
- `prompts/` — prompts de generación de imagen (ChatGPT/DALL-E/Midjourney) para cada
  corte y vista general, ya con las medidas y acabados exactos.

## Pendiente para la próxima sesión
1. Confirmar si va tanque de agua elevado por baño (el levantamiento previo detectó solo
   2 de las 4 vigas necesarias).
2. Confirmar tono exacto de microcemento y RAL de la pintura de piso.
3. Definir ventilación (afecta el secado de microcemento y epóxico, dado que no hay techo).
4. Cantidad de accesorios (dispensadores, ganchos) y si el banco lleva respaldo.
5. Render fotorrealista con Blender: bloqueado por política de red en el entorno usado
   hasta ahora — si se retoma desde un entorno sin esa restricción, el modelo 3D y el
   script de referencia de la skill `plano-tecnico` (render_blender.py) ya están listos
   para adaptar.
6. El usuario mencionó querer conectar SketchUp / Spline / Autodesk Fusion / Canva al
   flujo — ninguno tiene conector MCP en este entorno; Canva está listada pero sin
   autorizar. El .obj ya es el puente manual hacia SketchUp/Fusion mientras tanto.
