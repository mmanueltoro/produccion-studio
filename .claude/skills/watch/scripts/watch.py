#!/usr/bin/env python3
"""Extrae fotogramas de un video y lo analiza con Gemini (clave en GEMINI_API_KEY)."""
import argparse, base64, json, os, pathlib, subprocess, sys, tempfile, urllib.request

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
PROMPT = (
    "Mira este video y responde en español, en Markdown: "
    "1) Objetivo del video. 2) Transcripción o resumen de lo dicho. "
    "3) Pasos numerados de lo que se hace, con herramientas y datos usados. "
    "4) Entradas y salidas. 5) Errores comunes o consejos que se mencionan."
)


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out")
    ap.add_argument("--fps", type=float, default=0.5)
    ap.add_argument("--max-frames", type=int, default=40)
    a = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("Falta GEMINI_API_KEY en el entorno.")

    src = a.source
    if src.startswith(("http://", "https://")):
        tmp = tempfile.mkdtemp()
        run(["yt-dlp", "-f", "mp4/best", "-o", f"{tmp}/video.%(ext)s", src])
        src = str(next(pathlib.Path(tmp).glob("video.*")))
    name = pathlib.Path(src).stem
    out = pathlib.Path(a.out or f"watch-out/{name}")
    frames = out / "frames"
    frames.mkdir(parents=True, exist_ok=True)

    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", f"fps={a.fps},scale=768:-2",
         "-frames:v", str(a.max_frames), str(frames / "f_%04d.jpg")])

    # Video comprimido y pequeño para enviarlo inline (audio incluido).
    small = out / "small.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=640:-2,fps=5",
         "-b:v", "300k", "-b:a", "48k", str(small)])
    if small.stat().st_size > 18 * 1024 * 1024:
        sys.exit("El video comprimido supera 18 MB; recorta el video o usa un clip más corto.")

    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "video/mp4", "data": base64.b64encode(small.read_bytes()).decode()}},
        {"text": PROMPT}]}]}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    (out / "analysis.md").write_text(text)
    print(f"Listo: {out}/analysis.md y {len(list(frames.glob('*.jpg')))} fotogramas en {frames}")


if __name__ == "__main__":
    main()
