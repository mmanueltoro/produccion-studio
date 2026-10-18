---
name: watch
description: Ver y analizar un video (archivo local o URL) y convertir lo que enseña en una nueva habilidad (SKILL.md) reutilizable. Úsala siempre que el usuario diga /watch, "mira este video", "ve este video", "aprende de este video", "haz una habilidad a partir de este video", o pase un enlace/archivo de video (mp4, mov, YouTube, etc.) para analizarlo, resumirlo o extraer pasos de él.
---

# watch

Ve un video, entiende el proceso que muestra y lo convierte en una habilidad reutilizable.

## Requisitos
- `ffmpeg` (fotogramas y audio). `yt-dlp` solo si el video es una URL.
- Variable de entorno `GEMINI_API_KEY` (clave de Google AI Studio). Nunca la escribas en archivos, commits ni mensajes; si falta, pídele al usuario que la guarde como secreto del entorno.

## Flujo
1. Ejecuta el analizador:
   `python3 .claude/skills/watch/scripts/watch.py <ruta-o-url> [--out DIR] [--fps 0.5]`
   Deja en `DIR` (por defecto `./watch-out/<nombre>/`): `frames/` (fotogramas), `analysis.md` (descripción paso a paso y transcripción de Gemini).
2. Lee `analysis.md` y mira unos cuantos fotogramas clave con Read para verificar lo que dice el análisis; no te fíes solo del texto.
3. Resume al usuario qué enseña el video (objetivo, pasos, herramientas, datos de entrada/salida).
4. Si el usuario quiere una habilidad: usa la habilidad `skill-creator` con ese resumen como punto de partida (nombre, cuándo se activa, pasos, formato de salida) y guarda el resultado en `.claude/skills/<nombre>/SKILL.md`.

## Notas
- Videos largos: baja `--fps` o pasa `--max-frames` para limitar fotogramas.
- Explica el porqué de cada paso en la habilidad generada, no solo la lista de acciones.
