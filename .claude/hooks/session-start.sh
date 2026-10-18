#!/bin/bash
set -euo pipefail

# Solo en sesiones cloud
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
pip install -q yt-dlp faster-whisper openai-whisper opencv-python-headless
(cd edicion-de-video && npm install --silent)
