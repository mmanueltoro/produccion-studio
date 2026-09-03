# -*- coding: utf-8 -*-
"""Inyecta marca de agua MundoXpress y QR de WhatsApp en un SVG de plano."""
import json, re
qr=json.load(open("/root/vp/qr.json"))

def qr_group(x,y,size,fondo="#FFFFFF",tinta="#191D21"):
    n=qr["n"]; s=size/n
    o=[f'<g transform="translate({x:.1f},{y:.1f})">',
       f'<rect x="-5" y="-5" width="{size+10:.1f}" height="{size+10:.1f}" fill="{fondo}" '
       'stroke="#39424A" stroke-width="1"/>']
    for gy,row in enumerate(qr["rows"]):
        gx=0
        while gx<n:
            if row[gx]=="1":
                x2=gx
                while x2+1<n and row[x2+1]=="1": x2+=1
                o.append(f'<rect x="{gx*s:.2f}" y="{gy*s:.2f}" width="{(x2-gx+1)*s:.2f}" '
                         f'height="{s:.2f}" fill="{tinta}"/>')
                gx=x2+1
            else: gx+=1
    o.append('</g>')
    return "".join(o)

WM_DEF = ('<pattern id="wm" width="300" height="150" patternUnits="userSpaceOnUse" '
 'patternTransform="rotate(-24)">'
 '<text x="0" y="34" font-family="Archivo,Helvetica,Arial" font-size="19" font-weight="800" '
 'fill="%(c)s" fill-opacity="%(o)s" letter-spacing="1">MUNDOXPRESS</text>'
 '<text x="0" y="52" font-family="IBM Plex Mono,Courier New,monospace" font-size="11.5" '
 'fill="%(c)s" fill-opacity="%(o)s" letter-spacing="2.2">MANUEL TORO</text>'
 '<text x="150" y="112" font-family="Archivo,Helvetica,Arial" font-size="19" font-weight="800" '
 'fill="%(c)s" fill-opacity="%(o)s" letter-spacing="1">MUNDOXPRESS</text>'
 '<text x="150" y="130" font-family="IBM Plex Mono,Courier New,monospace" font-size="11.5" '
 'fill="%(c)s" fill-opacity="%(o)s" letter-spacing="2.2">MANUEL TORO</text>'
 '</pattern>')

def marcar(svg, qr_size=78, color="#39424A", opac="0.055", qr_pos=None, cred=True):
    m=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    W,H=float(m.group(1)), float(m.group(2))
    defs=WM_DEF % {"c":color,"o":opac}
    if "<defs>" in svg:
        svg=svg.replace("<defs>","<defs>"+defs,1)
    else:
        svg=re.sub(r'(<svg[^>]*>)', r'\1<defs>'+defs+'</defs>', svg, count=1)
    # marca de agua justo detrás del contenido
    svg=re.sub(r'(</defs>)',
        r'\1<rect x="0" y="0" width="%.0f" height="%.0f" fill="url(#wm)" pointer-events="none"/>'
        % (W,H), svg, count=1)
    # QR + crédito arriba a la derecha
    if qr_pos is None: qr_pos=(W-qr_size-14, 14)
    extra=qr_group(qr_pos[0],qr_pos[1],qr_size)
    if cred:
        cx=qr_pos[0]+qr_size/2
        extra+=(f'<text x="{cx:.1f}" y="{qr_pos[1]+qr_size+15:.1f}" text-anchor="middle" '
                'font-family="Archivo,Helvetica,Arial" font-size="8.5" font-weight="800" '
                'fill="#39424A" letter-spacing=".4">MUNDOXPRESS</text>'
                f'<text x="{cx:.1f}" y="{qr_pos[1]+qr_size+25:.1f}" text-anchor="middle" '
                'font-family="IBM Plex Mono,Courier New,monospace" font-size="7.5" '
                'fill="#6B7178">0412 313 0243</text>')
    svg=svg.replace("</svg>", extra+"</svg>")
    return svg
