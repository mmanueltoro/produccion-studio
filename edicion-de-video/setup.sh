#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
pip install yt-dlp faster-whisper openai-whisper opencv-python-headless
npm install
command -v ffmpeg >/dev/null || echo "Falta ffmpeg: instálalo con tu gestor de paquetes"
