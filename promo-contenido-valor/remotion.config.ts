import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// Chromium preinstalado en el entorno (sin descarga)
Config.setBrowserExecutable("/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell");
Config.setChromiumOpenGlRenderer("swangle");
