# -*- coding: utf-8 -*-
import pickle, math
import sys
PKL=sys.argv[1] if len(sys.argv)>1 else "planta.pkl"
OUT=sys.argv[2] if len(sys.argv)>2 else "modelo.obj"
d=pickle.load(open(PKL,"rb"))
Z,MESAS=d["ZONAS"],d["MESAS"]
CONT=[(0,0),(12.35,0),(12.35,1.60),(14.56,1.60),(14.56,9.41),(11.51,9.41),
      (11.51,8.87),(8.14,8.87),(8.14,8.24),(3.22,8.24),(3.22,7.08),(0,7.08)]
COL=(2.60,0.85,1.45,1.60); ALT=2.70; T=0.16; VENT=(3.32,12.35); PR=(0.25,1.15)
V=[];F=[];G=[]
def box3(x,y,z,w,h,dp,name):
    i=len(V)+1
    for (dx,dy,dz) in [(0,0,0),(w,0,0),(w,0,dp),(0,0,dp),(0,h,0),(w,h,0),(w,h,dp),(0,h,dp)]:
        V.append((x+dx,y+dy,z+dz))
    G.append((name,len(F)))
    for a in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        F.append(tuple(i+k for k in a))
for k in range(len(CONT)):
    a,b=CONT[k],CONT[(k+1)%len(CONT)]
    if a[1]==0 and b[1]==0:
        box3(0,0,-T/2,VENT[0],ALT,T,"muro_tapiado_redes")
        box3(VENT[0],0,-T/2,VENT[1]-VENT[0],0.95,T,"antepecho_ventanal")
        box3(VENT[0],2.35,-T/2,VENT[1]-VENT[0],ALT-2.35,T,"dintel_ventanal")
        j=0
        while VENT[0]+j*1.20<=VENT[1]+0.01:
            box3(min(VENT[0]+j*1.20,VENT[1])-0.04,0.95,-0.065,0.08,1.40,0.13,"montante_aluminio")
            j+=1
        box3(VENT[0],0.95,-0.02,VENT[1]-VENT[0],1.40,0.04,"vidrio_ventanal")
        continue
    dx,dz=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dz)
    if L<0.01: continue
    ang=math.atan2(dz,dx); i=len(V)+1
    ux,uz=math.cos(ang),math.sin(ang); px,pz=-uz*T/2,ux*T/2
    pts=[(a[0]+ux*t+px*s, a[1]+uz*t+pz*s) for (t,s) in [(0,-1),(L,-1),(L,1),(0,1)]]
    for yy in (0,ALT):
        for (X,Zp) in pts: V.append((X,yy,Zp))
    G.append(("muro_perimetral",len(F)))
    F.append((i,i+1,i+2,i+3)); F.append((i+4,i+7,i+6,i+5))
    for k2 in range(4): F.append((i+k2,i+4+k2,i+4+(k2+1)%4,i+(k2+1)%4))
box3(COL[0],0,COL[1],COL[2],ALT,COL[3],"columna_estructural")
# ---- RODAPIÉ perimetral: el detalle que más delata un render sin él ----
RH,RS=0.085,0.018
for k in range(len(CONT)):
    a,b=CONT[k],CONT[(k+1)%len(CONT)]
    dx,dz=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dz)
    if L<0.05: continue
    ux,uz=dx/L,dz/L; nx,nz=-uz,ux          # normal hacia el interior
    i=len(V)+1
    for (t,off) in [(0,0),(L,0),(L,RS),(0,RS)]:
        V.append((a[0]+ux*t+nx*off, 0.0, a[1]+uz*t+nz*off))
    for (t,off) in [(0,0),(L,0),(L,RS),(0,RS)]:
        V.append((a[0]+ux*t+nx*off, RH, a[1]+uz*t+nz*off))
    G.append(("RODAPIE",len(F)))
    F.append((i,i+1,i+2,i+3)); F.append((i+4,i+7,i+6,i+5))
    for q in range(4): F.append((i+q,i+4+q,i+4+(q+1)%4,i+(q+1)%4))
# rodapié también en la columna
for (ax,az,bx,bz) in [(COL[0],COL[1],COL[0]+COL[2],COL[1]),
                      (COL[0]+COL[2],COL[1],COL[0]+COL[2],COL[1]+COL[3]),
                      (COL[0]+COL[2],COL[1]+COL[3],COL[0],COL[1]+COL[3]),
                      (COL[0],COL[1]+COL[3],COL[0],COL[1])]:
    dx,dz=bx-ax,bz-az; L=math.hypot(dx,dz); ux,uz=dx/L,dz/L; nx,nz=uz,-ux
    i=len(V)+1
    for (t,off) in [(0,0),(L,0),(L,RS),(0,RS)]:
        V.append((ax+ux*t+nx*off,0.0,az+uz*t+nz*off))
    for (t,off) in [(0,0),(L,0),(L,RS),(0,RS)]:
        V.append((ax+ux*t+nx*off,RH,az+uz*t+nz*off))
    G.append(("RODAPIE",len(F)))
    F.append((i,i+1,i+2,i+3)); F.append((i+4,i+7,i+6,i+5))
    for q in range(4): F.append((i+q,i+4+q,i+4+(q+1)%4,i+(q+1)%4))
for z in Z:
    r=z["r"]
    if z["k"]=="redes":
        box3(r[0]+r[2]-T/2,0,r[1],T,ALT,r[3],"tabique_redes_este")
        box3(r[0],0,r[1]+r[3]-T/2,PR[0],ALT,T,"tabique_redes_sur_a")
        box3(PR[1],0,r[1]+r[3]-T/2,r[2]-PR[1],ALT,T,"tabique_redes_sur_b")
        box3(PR[0],2.10,r[1]+r[3]-T/2,PR[1]-PR[0],ALT-2.10,T,"dintel_puerta_redes")
        box3(PR[0],0,r[1]+r[3]+0.03,PR[1]-PR[0],2.05,0.05,"HOJA_PUERTA_REDES")
    elif z["k"]=="reunion":
        box3(r[0],0,r[1]+r[3]-0.015,r[2],ALT,0.03,"vidrio_sala_sur")
        box3(r[0]+r[2]-0.015,0,r[1],0.03,ALT,r[3],"vidrio_sala_este")
    elif z["k"]=="pecera":
        box3(r[0]-0.015,0,r[1],0.03,ALT,r[3],"vidrio_pecera")
def cyl(cx,y,cz,r,h,name,seg=10):
    import math as _m
    i=len(V)+1
    for yy in (y,y+h):
        for k in range(seg):
            a=2*_m.pi*k/seg; V.append((cx+r*_m.cos(a), yy, cz+r*_m.sin(a)))
    G.append((name,len(F)))
    for k in range(seg):
        k2=(k+1)%seg
        F.append((i+k, i+k2, i+seg+k2, i+seg+k))
    F.append(tuple(i+k for k in range(seg)))
    F.append(tuple(i+seg+k for k in range(seg-1,-1,-1)))

def _rot(cx,cz,rot,dx,dz):
    import math as _m
    ca,sa=_m.cos(rot),_m.sin(rot)
    return (cx+dx*ca+dz*sa, cz-dx*sa+dz*ca)

def caja_rot(cx,cz,rot,dx,dz,y,w,h,d,name):
    """caja centrada en (dx,dz) local, girada. Aproximada a ejes cuando rot es recto."""
    import math as _m
    px,pz=_rot(cx,cz,rot,dx,dz)
    if abs(_m.sin(rot))<0.5: box3(px-w/2,y,pz-d/2,w,h,d,name)
    else:                    box3(px-d/2,y,pz-w/2,d,h,w,name)

def silla(cx,cz,rot,name="SILLA"):
    """Silla operativa: base de 5 radios, columna, asiento y respaldo con reclinación.
    rot: 0 respaldo al norte · pi al sur · pi/2 oeste · -pi/2 este"""
    import math as _m
    # base de 5 radios con rueda en cada punta
    for k in range(5):
        an=2*_m.pi*k/5 + rot
        rx,rz=cx+0.24*_m.cos(an), cz+0.24*_m.sin(an)
        i=len(V)+1
        for (dx,dz) in [(-0.028,-0.028),(0.028,-0.028),(0.028,0.028),(-0.028,0.028)]:
            V.append((cx+dx,0.055,cz+dz))
        for (dx,dz) in [(-0.022,-0.022),(0.022,-0.022),(0.022,0.022),(-0.022,0.022)]:
            V.append((rx+dx,0.045,rz+dz))
        G.append(("base_silla",len(F)))
        F.append((i,i+1,i+2,i+3)); F.append((i+4,i+7,i+6,i+5))
        for q in range(4): F.append((i+q,i+4+q,i+4+(q+1)%4,i+(q+1)%4))
        cyl(rx,0.0,rz,0.032,0.045,"rueda_silla",8)
    cyl(cx,0.05,cz,0.048,0.06,"base_silla",10)
    cyl(cx,0.11,cz,0.032,0.30,"columna_silla",10)      # pistón
    cyl(cx,0.41,cz,0.055,0.04,"columna_silla",10)      # mecanismo
    # asiento: dos piezas para que no sea un ladrillo
    caja_rot(cx,cz,rot,0,0.01,0.45,0.47,0.055,0.45,name)
    caja_rot(cx,cz,rot,0,0.19,0.44,0.43,0.045,0.11,name)   # borde delantero rebajado
    # respaldo: marco perimetral + panel de malla hundido
    for (dz,y,h) in [(-0.205,0.52,0.15),(-0.222,0.67,0.16),(-0.242,0.83,0.14)]:
        for lado in (-1,1):                                  # montantes
            caja_rot(cx,cz,rot,lado*0.205,dz,y,0.032,h,0.038,"marco_silla")
        caja_rot(cx,cz,rot,0,dz,y,0.38,h,0.016,name)         # malla, más delgada
    caja_rot(cx,cz,rot,0,-0.245,0.955,0.44,0.035,0.042,"marco_silla")   # cabecero
    caja_rot(cx,cz,rot,0,-0.19,0.50,0.11,0.09,0.05,"marco_silla")       # soporte lumbar
    # apoyabrazos en L
    for lado in (-1,1):
        caja_rot(cx,cz,rot,lado*0.255,-0.02,0.50,0.045,0.17,0.30,"brazo_silla")
        caja_rot(cx,cz,rot,lado*0.255,0.00,0.67,0.055,0.035,0.26,"brazo_silla")

def mueble(cx,cz,w,dp,h,name,y0=0):
    box3(cx-w/2,y0+h-0.04,cz-dp/2,w,0.04,dp,name)
    for (sx,sz) in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        box3(cx+sx*(w/2-0.09)-0.025,y0,cz+sz*(dp/2-0.09)-0.025,0.05,h-0.04,0.05,"pata")
SI=0.78
import math as _mm
for m in MESAS:
    n=max(1,m["pl"]//2)
    if m["rot"]:
        w=m["fw"]-2*SI; dp=m["fh"]
        mueble(m["x"]+SI+w/2,m["y"]+dp/2,w,dp,0.75,f"mesa_{m['pl']}pax")
        if m["pl"]==1: silla(m["x"]+SI-0.40, m["y"]+dp/2, _mm.pi/2)
        else:
            for k in range(n):
                cz=m["y"]+dp*(k+0.5)/n
                silla(m["x"]+SI-0.40,cz,_mm.pi/2); silla(m["x"]+SI+w+0.40,cz,-_mm.pi/2)
    else:
        w=m["fw"]; dp=m["fh"]-2*SI
        mueble(m["x"]+w/2,m["y"]+SI+dp/2,w,dp,0.75,f"mesa_{m['pl']}pax")
        if m["pl"]==1: silla(m["x"]+w/2, m["y"]+SI-0.40, 0)
        else:
            for k in range(n):
                cx=m["x"]+w*(k+0.5)/n
                silla(cx,m["y"]+SI-0.40,0); silla(cx,m["y"]+SI+dp+0.40,_mm.pi)
for (fijo,x0,nb) in [(8.24,3.55,2),(8.87,8.30,3)]:
    mueble(x0+nb*0.40,fijo-0.30,nb*0.80,0.60,0.75,f"barra_muro_{nb}pax")
    for k in range(nb): silla(x0+nb*0.80*(k+0.5)/nb, fijo-1.05, _mm.pi)
S=Z[1]["r"]; mueble(S[0]+0.85+1.90,S[1]+1.65,3.80,1.20,0.75,"mesa_reuniones_10pax")
for k in range(4):
    cxx=S[0]+0.85+3.80*(k+0.5)/4
    silla(cxx,S[1]+1.05-0.42,0); silla(cxx,S[1]+1.05+1.20+0.42,_mm.pi)
silla(S[0]+0.85-0.42,S[1]+1.65,_mm.pi/2); silla(S[0]+0.85+3.80+0.42,S[1]+1.65,-_mm.pi/2)
mueble(1.40,6.78,2.20,0.60,0.90,"punto_cafe")
for r in [z["r"] for z in Z if z["k"]=="pecera"]:
    mueble(r[0]+1.42,r[1]+2.81,1.85,0.82,0.75,"escritorio_pecera")
    silla(r[0]+1.42,r[1]+1.95,_mm.pi)
    silla(r[0]+0.95,r[1]+3.67,0); silla(r[0]+1.95,r[1]+3.67,0)
    box3(r[0]+2.55,0,r[1]+0.40,0.42,1.10,1.30,"credenza_pecera")
for k in range(4): box3(0.28+k*0.66,0,2.30,0.58,2.00,1.15,"rack_42U")
box3(0.28,0,0.30,1.00,1.20,0.72,"ups"); box3(1.45,0,0.30,0.62,1.60,0.72,"tablero")
mueble(2.13,4.11,1.55,0.62,0.95,"mueble_impresion")
# --- PISO y TECHO (triangulación del contorno) ---
from shapely.geometry import Polygon, Point
from shapely.ops import triangulate as _tri
poly=Polygon(CONT)
tris=[t for t in _tri(poly) if poly.contains(t.representative_point())]
for (yy,nm,inv) in [(0.0,"PISO_laminado_click",False),(ALT,"TECHO_drywall",True)]:
    G.append((nm,len(F)))
    for t in tris:
        c=list(t.exterior.coords)[:3]
        i=len(V)+1
        for (X,Zp) in c: V.append((X,yy,Zp))
        F.append((i,i+2,i+1) if inv else (i,i+1,i+2))
print(f"piso y techo: {len(tris)} triángulos cada uno")

# ================= UTILERÍA: lo que hace que un render parezca real =================
import math as _u
def esfera(cx,cy,cz,r,name,seg=8,ring=5):
    i=len(V)+1
    for j in range(1,ring):
        phi=_u.pi*j/ring
        for a in range(seg):
            an=2*_u.pi*a/seg
            V.append((cx+r*_u.sin(phi)*_u.cos(an), cy+r*0.82*_u.cos(phi),
                      cz+r*_u.sin(phi)*_u.sin(an)))
    top=len(V)+1; V.append((cx,cy+r*0.82,cz))
    bot=len(V)+1; V.append((cx,cy-r*0.82,cz))
    G.append((name,len(F)))
    for j in range(ring-2):
        for a in range(seg):
            a2=(a+1)%seg
            F.append((i+j*seg+a, i+j*seg+a2, i+(j+1)*seg+a2, i+(j+1)*seg+a))
    for a in range(seg):
        a2=(a+1)%seg
        F.append((top, i+a2, i+a))
        F.append((bot, i+(ring-2)*seg+a, i+(ring-2)*seg+a2))

def maceta(cx,cz,alto=1.35,r=0.24,name="PLANTA"):
    cyl(cx,0,cz,r,0.36,"maceta")                       # tiesto
    cyl(cx,0.36,cz,r*0.55,0.16,"tierra")
    t=alto-0.52
    cyl(cx,0.52,cz,0.032,t*0.55,"tronco")
    # follaje: varias masas esféricas achatadas, desfasadas
    for (dx,dy,dz,rr) in [(0,0.62,0,0.34),(0.20,0.48,0.10,0.25),(-0.18,0.52,-0.12,0.24),
                          (0.06,0.80,-0.16,0.22),(-0.10,0.75,0.16,0.20)]:
        esfera(cx+dx*(alto/1.4), 0.52+t*dy, cz+dz*(alto/1.4), rr*(alto/1.4), name)
def papelera(cx,cz):
    cyl(cx,0,cz,0.16,0.42,"PAPELERA")
def monitor(cx,cz,rot=0):
    """Carcasa negra + panel ligeramente hundido. El panel mira al usuario."""
    ca,sa=_u.cos(rot),_u.sin(rot)
    cyl(cx,0.75,cz,0.075,0.025,"monitor_base")
    cyl(cx,0.775,cz,0.019,0.135,"monitor_cuello")
    # rot=0 -> respaldo de la silla al norte -> el usuario mira al sur -> panel hacia el sur (+z)
    frente = 1 if abs(sa)<0.5 and ca>0 else (-1 if abs(sa)<0.5 else 0)
    if abs(sa)<0.5:
        f = 1 if ca>0 else -1
        box3(cx-0.215,0.905,cz-0.016,0.43,0.265,0.032,"monitor_carcasa")
        box3(cx-0.198,0.921,cz+(0.016*f)-0.004,0.396,0.233,0.004,"MONITOR_PANEL")
    else:
        f = 1 if sa>0 else -1
        box3(cx-0.016,0.905,cz-0.215,0.032,0.265,0.43,"monitor_carcasa")
        box3(cx+(0.016*f)-0.004,0.921,cz-0.198,0.004,0.233,0.396,"MONITOR_PANEL")
def taza(cx,cz): cyl(cx,0.755,cz,0.042,0.095,"taza")
def cuaderno(cx,cz,w=0.21,d=0.29): box3(cx-w/2,0.755,cz-d/2,w,0.012,d,"cuaderno")
def lampara_pie(cx,cz):
    cyl(cx,0,cz,0.20,0.03,"lampara_base"); cyl(cx,0.03,cz,0.022,1.55,"lampara_vastago")
    cyl(cx,1.58,cz,0.19,0.28,"LAMPARA_PANTALLA")

# plantas en los rincones que quedan libres
for (px,pz,al) in [(0.55,6.55,1.55),(9.90,1.05,1.35),(10.90,8.35,1.65),
                   (3.60,7.55,1.25),(13.95,5.15,1.30)]:
    maceta(px,pz,al)
# planta baja sobre la credenza de cada pecera
for r in [z["r"] for z in Z if z["k"]=="pecera"]:
    cyl(r[0]+2.76,1.10,r[1]+0.75,0.11,0.14,"maceta")
    cyl(r[0]+2.76,1.24,r[1]+0.75,0.19,0.26,"PLANTA")
# papeleras
for (px,pz) in [(3.05,4.95),(9.95,7.95),(11.95,5.05),(11.95,8.95),(0.42,7.35)]:
    papelera(px,pz)
# lámpara de pie en el rincón de café
lampara_pie(2.85,6.62)
# monitores, tazas y cuadernos en los puestos de trabajo
for m in MESAS:
    nn=max(1,m["pl"]//2)
    if m["rot"]:
        w=m["fw"]-2*SI; dp=m["fh"]
        for k in range(nn):
            cz=m["y"]+dp*(k+0.5)/nn
            monitor(m["x"]+SI+0.32,cz,_u.pi/2); monitor(m["x"]+SI+w-0.32,cz,-_u.pi/2)
    else:
        w=m["fw"]; dp=m["fh"]-2*SI
        for k in range(nn):
            cx=m["x"]+w*(k+0.5)/nn
            monitor(cx,m["y"]+SI+0.30,0); monitor(cx,m["y"]+SI+dp-0.30,_u.pi)
        taza(m["x"]+0.30, m["y"]+SI+0.30)
        cuaderno(m["x"]+w-0.32, m["y"]+SI+dp-0.34)
# sobre la mesa de reuniones
taza(S[0]+1.35,S[1]+1.35); taza(S[0]+3.90,S[1]+2.05)
cuaderno(S[0]+2.10,S[1]+1.35); cuaderno(S[0]+3.20,S[1]+2.00)
# en los escritorios de las peceras
for r in [z["r"] for z in Z if z["k"]=="pecera"]:
    monitor(r[0]+1.42, r[1]+2.55, 0); taza(r[0]+0.75, r[1]+2.60)

lines=["# VP Emvepro - modelo 3D a escala real, en metros",
 "# MundoXpress - Manuel Toro - 0412 313 0243",
 "# Area util 116.07 m2 · altura libre 2.70 m · 21 personas",
 "# Ejes: X este, Y arriba, Z sur. Origen en la esquina noroeste del local.",
 "# Piso: laminado click, tablilla de 0.19 m. Mobiliario: roble miel."]
for (x,y,z) in V: lines.append(f"v {x:.4f} {y:.4f} {z:.4f}")
gi=0
for i,f in enumerate(F):
    while gi<len(G) and G[gi][1]==i: lines.append(f"g {G[gi][0]}"); gi+=1
    lines.append("f "+" ".join(str(k) for k in f))
open(OUT,"w").write("\n".join(lines)+"\n")
print(f"OBJ: {len(V)} vértices · {len(F)} caras · {len(set(g[0] for g in G))} objetos nombrados")
