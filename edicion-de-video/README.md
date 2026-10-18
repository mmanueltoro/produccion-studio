# Edición de video

Herramientas para editar video (flujo del video de referencia, paso 3 "Copia los repos").

| Herramienta | Para qué | Instalación |
|---|---|---|
| FFmpeg | cortes, recortes, mezcla y render | `apt install ffmpeg` (sistema) |
| faster-whisper | transcripción palabra por palabra | `pip install faster-whisper` |
| openai/whisper | modelo de voz que usa faster-whisper | `pip install openai-whisper` |
| yt-dlp | bajar el video de referencia | `pip install yt-dlp` |
| OpenCV | seguir a quien habla en el recorte vertical | `pip install opencv-python-headless` |
| Puppeteer | renderizar subtítulos y títulos | `npm i puppeteer` |
| HyperFrames (HeyGen) | motion graphics desde HTML | `npm i hyperframes` |

Instalar todo: `bash setup.sh`

## Carpetas
- `entrada/` videos de origen
- `salida/` renders finales
- `scripts/` scripts de edición
