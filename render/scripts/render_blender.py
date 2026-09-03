# -*- coding: utf-8 -*-
"""Render fotorrealista del local VP Emvepro con Cycles."""
import bpy, math, sys, os
from mathutils import Vector

ARGS = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
VISTA = ARGS[0] if ARGS else "A"
SAMPLES = int(ARGS[1]) if len(ARGS)>1 else 64
RES = (int(ARGS[2]), int(ARGS[3])) if len(ARGS)>3 else (1400, 900)
OUT = ARGS[4] if len(ARGS)>4 else f"vista_{VISTA}.png"

# ---------- limpiar ----------
bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------- importar ----------
OBJ = os.environ.get("MODELO_OBJ","modelo.obj")
bpy.ops.wm.obj_import(filepath=OBJ,
                      use_split_groups=True, forward_axis='NEGATIVE_Z', up_axis='Y')
print(f"objetos importados: {len(bpy.data.objects)}")

# ---------- materiales ----------
def mat(nombre, base, rough=0.8, metal=0.0, trans=0.0, ior=1.45, emis=None, emis_str=0):
    m = bpy.data.materials.new(nombre); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if trans:
        b.inputs["Transmission Weight"].default_value = trans
        b.inputs["IOR"].default_value = ior
        m.use_backface_culling = False
        m.blend_method = 'BLEND'
    if emis:
        b.inputs["Emission Color"].default_value = (*emis, 1)
        b.inputs["Emission Strength"].default_value = emis_str
    return m

def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple((x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4) for x in c)

M_PISO  = mat("piso_roble",   srgb("A8763F"), 0.38)
def piso_listones(m):
    nt=m.node_tree; b=nt.nodes["Principled BSDF"]
    tc=nt.nodes.new("ShaderNodeTexCoord")
    mp=nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(1,5.3,1)
    # veta larga en la dirección del listón
    veta=nt.nodes.new("ShaderNodeTexNoise")
    veta.inputs["Scale"].default_value=2.5; veta.inputs["Detail"].default_value=8
    vs=nt.nodes.new("ShaderNodeMapping"); vs.inputs["Scale"].default_value=(1.2,26,1)
    ramp=nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position=0.34
    ramp.color_ramp.elements[0].color=(*srgb("A0703C"),1)
    ramp.color_ramp.elements[1].position=0.68
    ramp.color_ramp.elements[1].color=(*srgb("CFA067"),1)
    # junta entre tablillas
    junta=nt.nodes.new("ShaderNodeTexWave"); junta.wave_type='BANDS'
    junta.bands_direction='Y'; junta.inputs["Scale"].default_value=5.3
    junta.inputs["Distortion"].default_value=0
    jr=nt.nodes.new("ShaderNodeValToRGB")
    jr.color_ramp.elements[0].position=0.02; jr.color_ramp.elements[1].position=0.09
    mix=nt.nodes.new("ShaderNodeMixRGB"); mix.blend_type='MULTIPLY'
    mix.inputs["Fac"].default_value=0.55
    bump=nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.14
    nt.links.new(tc.outputs["Object"], vs.inputs["Vector"])
    nt.links.new(vs.outputs["Vector"], veta.inputs["Vector"])
    nt.links.new(veta.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], junta.inputs["Vector"])
    nt.links.new(junta.outputs["Fac"], jr.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], mix.inputs["Color1"])
    nt.links.new(jr.outputs["Color"], mix.inputs["Color2"])
    nt.links.new(mix.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(jr.outputs["Color"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value=0.30
piso_listones(M_PISO)
M_BLANCO= mat("blanco_mate",  srgb("F2EFE9"), 0.92)
M_TECHO = mat("techo",        srgb("FAF8F5"), 0.95)
M_ALU   = mat("aluminio",     srgb("9AA1A7"), 0.40, metal=0.85)
M_VIDRIO= mat("vidrio",       srgb("F4F8FA"), 0.02, trans=1.0, ior=1.45)
M_ROBLE = mat("roble_miel",   srgb("A06E33"), 0.34)
def veta(m, esc=(3,34,1)):
    nt=m.node_tree; b=nt.nodes["Principled BSDF"]
    tc=nt.nodes.new("ShaderNodeTexCoord"); mp=nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value=esc
    nz=nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value=3.0; nz.inputs["Detail"].default_value=9
    rp=nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].position=0.38
    rp.color_ramp.elements[0].color=(*srgb("8A5C28"),1)
    rp.color_ramp.elements[1].position=0.64
    rp.color_ramp.elements[1].color=(*srgb("B8854A"),1)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"])
    nt.links.new(rp.outputs["Color"], b.inputs["Base Color"])
veta(M_ROBLE)
M_NEGRO = mat("negro_mate",   srgb("232629"), 0.55, metal=0.30)
M_RACK  = mat("grafito",      srgb("2E3338"), 0.45, metal=0.55)
M_SILLA = mat("silla_malla", srgb("2B2E33"), 0.72)
M_HOJA  = mat("follaje",     srgb("3E6B3A"), 0.68)
M_TIESTO= mat("tiesto",      srgb("6E6A63"), 0.80)
M_TIERRA= mat("tierra",      srgb("3A2E24"), 0.95)
M_TRONCO= mat("tronco",      srgb("6B5136"), 0.85)
M_PANT  = mat("pantalla",    srgb("10151A"), 0.14,
                             emis=srgb("38566B"), emis_str=0.20)
M_CARC  = mat("carcasa_monitor", srgb("1C1F23"), 0.42)
M_RODA  = mat("rodapie",     srgb("EDE9E2"), 0.45)
M_MARCO = mat("marco_silla", srgb("1A1D21"), 0.38, metal=0.45)
M_CERAM = mat("ceramica",    srgb("EFEBE4"), 0.35)
M_PAPEL = mat("papel",       srgb("E8E3D8"), 0.85)
M_LAMP  = mat("pantalla_lampara", srgb("F2EDE2"), 0.75,
              emis=srgb("FFEFD6"), emis_str=2.2)
M_LED   = mat("led",          srgb("EAF4FF"), 0.5, emis=srgb("EAF4FF"), emis_str=1.15)

REGLAS = [
 ("PISO_", M_PISO), ("TECHO_", M_TECHO),
 ("muro_", M_BLANCO), ("tabique_", M_BLANCO), ("columna_", M_BLANCO),
 ("dintel_", M_BLANCO), ("antepecho_", M_BLANCO), ("HOJA_PUERTA", M_BLANCO),
 ("montante_aluminio", M_ALU),
 ("vidrio_", M_VIDRIO),
 ("mesa_", M_ROBLE), ("barra_muro", M_ROBLE), ("escritorio_", M_ROBLE),
 ("credenza_", M_ROBLE), ("punto_cafe", M_ROBLE), ("mueble_impresion", M_ROBLE),
 ("RODAPIE", M_RODA), ("marco_silla", M_MARCO), ("SILLA", M_SILLA),
 ("PLANTA", M_HOJA), ("maceta", M_TIESTO), ("tierra", M_TIERRA), ("tronco", M_TRONCO),
 ("PAPELERA", M_RACK), ("MONITOR_PANEL", M_PANT), ("monitor_carcasa", M_CARC), ("monitor_", M_NEGRO),
 ("taza", M_CERAM), ("cuaderno", M_PAPEL),
 ("LAMPARA_PANTALLA", M_LAMP), ("lampara_", M_NEGRO), ("pata_silla", M_NEGRO), ("base_silla", M_NEGRO), ("rueda_silla", M_NEGRO),
 ("columna_silla", M_NEGRO), ("brazo_silla", M_NEGRO),
 ("pata", M_NEGRO),
 ("rack_", M_RACK), ("ups", M_RACK), ("tablero", M_RACK),
]
sin = []
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    o.data.materials.clear()
    for pref, m in REGLAS:
        if o.name.startswith(pref) or pref in o.name:
            o.data.materials.append(m); break
    else:
        o.data.materials.append(M_BLANCO); sin.append(o.name)
if sin: print("sin material específico:", sin[:6])

# BISEL: ningún objeto real tiene el canto perfectamente vivo
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    bv = o.modifiers.new("bisel", 'BEVEL')
    bv.width = 0.004 if o.name.startswith(("vidrio","PISO","TECHO","muro","tabique")) else 0.010
    bv.segments = 2; bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(35)
    bv.harden_normals = False
    if not o.name.startswith(("PISO","TECHO","muro","tabique","vidrio")):
        for p in o.data.polygons: p.use_smooth = False

# ---------- luces ----------
# En Blender tras la conversión: X este, Y = norte (el ventanal está en y=0), Z arriba.
sol = bpy.data.lights.new("sol", 'SUN'); sol.energy = 3.8
sol.angle = math.radians(2.5); sol.color = (1.0, 0.96, 0.90)
so = bpy.data.objects.new("sol", sol); bpy.context.collection.objects.link(so)
so.rotation_euler = (math.radians(52), 0, math.radians(-28))   # entra por el ventanal
so.location = (6, 9, 8)

cielo = bpy.data.worlds.new("mundo"); bpy.context.scene.world = cielo
cielo.use_nodes = True
nt = cielo.node_tree
bg = nt.nodes["Background"]
HDRI = os.environ.get("HDRI","cielo.hdr")
if os.path.exists(HDRI):
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(HDRI)
    mp = nt.nodes.new("ShaderNodeMapping")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp.inputs["Rotation"].default_value[2] = math.radians(-40)
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs[1].default_value = 0.72
    print("HDRI cargado")
else:
    # Sin HDRI: cielo físico (Nishita) alineado con el sol de la escena. Da luz azulada
    # de cielo + horizonte cálido; mucho mejor que un color plano.
    sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = 'NISHITA'
    sky.sun_elevation = math.radians(44); sky.sun_rotation = math.radians(-28)
    sky.sun_intensity = 0.0          # el sol lo pone la lámpara SUN, no el cielo
    sky.altitude = 900               # Caracas, aprox.
    sky.air_density = 1.0; sky.dust_density = 0.45
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    bg.inputs[1].default_value = 0.045
    print("HDRI no encontrado: cielo procedural Nishita")

def led(x0, x1, y, alto=2.58):
    l = bpy.data.lights.new("led", 'AREA'); l.shape='RECTANGLE'
    l.size = x1-x0; l.size_y = 0.055
    l.energy = 7 * (x1-x0); l.color = (0.90, 0.95, 1.0)
    o = bpy.data.objects.new("led", l); bpy.context.collection.objects.link(o)
    o.location = ((x0+x1)/2, -y, alto); o.rotation_euler = (math.pi, 0, 0)
rel = bpy.data.lights.new("relleno",'AREA'); rel.shape='RECTANGLE'
rel.size=9.0; rel.size_y=5.0; rel.energy=140; rel.color=(0.95,0.96,1.0)
ro = bpy.data.objects.new("relleno", rel); bpy.context.collection.objects.link(ro)
ro.location=(7.0,-5.0,2.62); ro.rotation_euler=(math.pi,0,0)
for a,b,y in [(4.6,10.2,4.35),(4.6,10.2,5.95),(4.0,10.2,7.55),
              (0.30,2.90,1.10),(0.30,2.90,3.20),
              (4.10,8.00,1.20),(4.10,8.00,2.10),
              (11.9,14.2,3.00),(11.9,14.2,7.00)]:
    led(a,b,y)

# ---------- cámaras ----------
VISTAS = {
 "A":      dict(pos=(4.70, -7.70, 1.52), mira=(8.60, -2.30, 1.05), lente=26),
 "B":      dict(pos=(5.60, -1.15, 1.52), mira=(13.00, -7.20, 1.05), lente=30),
 "cenital":dict(pos=(7.28, -4.70, 13.0), mira=(7.28, -4.71, 0.0),  lente=20),
}
v = VISTAS[VISTA]
cam = bpy.data.cameras.new("cam"); cam.lens = v["lente"]
cam.sensor_width = 36
co = bpy.data.objects.new("cam", cam); bpy.context.collection.objects.link(co)
co.location = v["pos"]
d = Vector(v["mira"]) - Vector(v["pos"])
co.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
if VISTA != "cenital":                       # verticales rectas: sin cabeceo
    co.rotation_euler.x = math.radians(90)
    cam.shift_y = -0.075                     # encuadra hacia abajo sin inclinar
if VISTA != "cenital":
    cam.dof.use_dof = True
    cam.dof.focus_distance = (Vector(v["mira"]) - Vector(v["pos"])).length * 0.72
    cam.dof.aperture_fstop = 5.6
bpy.context.scene.camera = co
# en cenital escondemos el techo
if VISTA == "cenital":
    for o in bpy.data.objects:
        if o.name.startswith("TECHO"): o.hide_render = True
    co.rotation_euler = (0, 0, 0)      # alineada con el plano: ventanal arriba

# ---------- render ----------
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
sc.cycles.denoising_prefilter = 'ACCURATE'
sc.cycles.max_bounces = 8
sc.cycles.transmission_bounces = 6
sc.cycles.caustics_reflective = False
sc.cycles.caustics_refractive = False
sc.render.resolution_x, sc.render.resolution_y = RES
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.view_settings.exposure = 0.32
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = OUT
print(f"render {VISTA} · {RES[0]}x{RES[1]} · {SAMPLES} samples -> {OUT}")
bpy.ops.render.render(write_still=True)
print("LISTO", OUT)
