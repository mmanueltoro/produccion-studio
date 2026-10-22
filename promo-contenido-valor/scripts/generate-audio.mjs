// Genera música + efectos de sonido por síntesis pura (sin samples externos).
// Salida: public/audio/music.wav, public/audio/sfx.wav, public/audio/mix.wav
import { writeFileSync, mkdirSync } from "node:fs";

const SR = 48000;
const DUR = 10;
const N = SR * DUR;

const mk = () => new Float32Array(N);
const clamp = (x) => Math.max(-1, Math.min(1, x));
const noteHz = (semi) => 440 * Math.pow(2, (semi - 69) / 12);

// ---------- utilidades ----------
function env(t, a, d, s, r, len) {
  // ADSR simple en segundos, len = duración total de la nota
  if (t < 0) return 0;
  if (t < a) return t / a;
  if (t < a + d) return 1 - (1 - s) * ((t - a) / d);
  if (t < len - r) return s;
  if (t < len) return s * (1 - (t - (len - r)) / r);
  return 0;
}
function addTone(buf, start, len, hz, gain, { wave = "sine", a = 0.01, d = 0.1, s = 0.7, r = 0.1, detune = 0 } = {}) {
  const i0 = Math.floor(start * SR);
  const i1 = Math.min(N, Math.floor((start + len) * SR));
  for (let i = i0; i < i1; i++) {
    const t = (i - i0) / SR;
    const ph = 2 * Math.PI * hz * (1 + detune) * t;
    let v;
    if (wave === "sine") v = Math.sin(ph);
    else if (wave === "tri") v = (2 / Math.PI) * Math.asin(Math.sin(ph));
    else if (wave === "saw") v = 2 * ((hz * t) % 1) - 1;
    else v = Math.sign(Math.sin(ph));
    buf[i] += v * gain * env(t, a, d, s, r, len);
  }
}
// pasa-bajos de un polo (para suavizar sierras)
function lowpass(buf, cutoff) {
  const rc = 1 / (2 * Math.PI * cutoff);
  const dt = 1 / SR;
  const alpha = dt / (rc + dt);
  let y = 0;
  for (let i = 0; i < buf.length; i++) {
    y += alpha * (buf[i] - y);
    buf[i] = y;
  }
}
let seed = 1337;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;

// ---------- MÚSICA: pulso de autoridad, Dm, 120 BPM ----------
const music = mk();
const BPM = 120;
const beat = 60 / BPM; // 0.5 s
// progresión por compás (2 s): Dm - Bb - F - C - Dm
const chords = [
  [50, 53, 57], // Dm (D3 F3 A3)
  [46, 50, 53], // Bb
  [41, 45, 48], // F
  [48, 52, 55], // C
  [50, 53, 57], // Dm
];
// Bajo: nota raíz en cada beat, sub + sierra filtrada
const bass = mk();
for (let bar = 0; bar < 5; bar++) {
  const root = chords[bar][0] - 12;
  for (let b = 0; b < 4; b++) {
    const t0 = bar * 2 + b * beat;
    addTone(bass, t0, beat * 0.9, noteHz(root), 0.42, { wave: "sine", a: 0.005, d: 0.15, s: 0.6, r: 0.08 });
    addTone(bass, t0, beat * 0.9, noteHz(root), 0.18, { wave: "saw", a: 0.005, d: 0.2, s: 0.3, r: 0.08 });
  }
}
lowpass(bass, 220);
// Pad: acorde sostenido, dos sierras desafinadas, filtrado
const pad = mk();
for (let bar = 0; bar < 5; bar++) {
  for (const n of chords[bar]) {
    addTone(pad, bar * 2, 2.05, noteHz(n + 12), 0.07, { wave: "saw", a: 0.4, d: 0.3, s: 0.8, r: 0.5, detune: 0.004 });
    addTone(pad, bar * 2, 2.05, noteHz(n + 12), 0.07, { wave: "saw", a: 0.4, d: 0.3, s: 0.8, r: 0.5, detune: -0.004 });
  }
}
lowpass(pad, 900);
// Arpegio en corcheas: brillo tipo "ticker" de newsroom
const arp = mk();
for (let bar = 0; bar < 5; bar++) {
  const ch = chords[bar];
  for (let e = 0; e < 8; e++) {
    const t0 = bar * 2 + e * (beat / 2);
    const n = ch[e % 3] + 24 + (e >= 4 ? 12 : 0);
    addTone(arp, t0, 0.18, noteHz(n), 0.09, { wave: "tri", a: 0.003, d: 0.1, s: 0.2, r: 0.05 });
  }
}
// Hi-hat sintético en contratiempo + kick suave en cada beat
const drums = mk();
for (let b = 0; b < 20; b++) {
  const t0 = b * beat;
  const i0 = Math.floor(t0 * SR);
  // kick: seno con pitch descendente
  for (let i = 0; i < SR * 0.25; i++) {
    const t = i / SR;
    const f = 120 * Math.exp(-t * 18) + 45;
    drums[i0 + i] += Math.sin(2 * Math.PI * f * t) * Math.exp(-t * 14) * 0.5;
  }
  // hat en el "y"
  const ih = Math.floor((t0 + beat / 2) * SR);
  for (let i = 0; i < SR * 0.05; i++) {
    const t = i / SR;
    drums[ih + i] += rnd() * Math.exp(-t * 90) * 0.12;
  }
}
for (let i = 0; i < N; i++) music[i] = bass[i] + pad[i] + arp[i] + drums[i];
// Fade in 0.6 s / fade out últimos 1.4 s
for (let i = 0; i < N; i++) {
  const t = i / SR;
  let g = 1;
  if (t < 0.6) g = t / 0.6;
  if (t > DUR - 1.4) g = Math.min(g, (DUR - t) / 1.4);
  music[i] *= g * 0.9;
}

// ---------- SFX ----------
const sfx = mk();
function whoosh(at, len = 0.45, gain = 0.5) {
  // ruido con pasa-bajos cuya frecuencia sube y baja (sweep)
  const i0 = Math.floor(at * SR);
  let y = 0;
  for (let i = 0; i < len * SR && i0 + i < N; i++) {
    const t = i / len;
    const cutoff = 300 + 5000 * Math.sin(Math.PI * t) ** 2;
    const alpha = (1 / SR) / (1 / (2 * Math.PI * cutoff) + 1 / SR);
    y += alpha * (rnd() - y);
    const e = Math.sin(Math.PI * t) ** 1.5;
    sfx[i0 + i] += y * e * gain * 3;
  }
}
function pop(at, hz = 900, gain = 0.45) {
  // "pop": seno corto con pitch que cae + click
  const i0 = Math.floor(at * SR);
  for (let i = 0; i < SR * 0.09 && i0 + i < N; i++) {
    const t = i / SR;
    const f = hz * Math.exp(-t * 30) + hz * 0.4;
    sfx[i0 + i] += Math.sin(2 * Math.PI * f * t) * Math.exp(-t * 45) * gain;
    if (i < 40) sfx[i0 + i] += rnd() * 0.25 * gain;
  }
}
function hit(at) {
  // remate final: golpe grave + shimmer agudo
  const i0 = Math.floor(at * SR);
  for (let i = 0; i < SR * 1.6 && i0 + i < N; i++) {
    const t = i / SR;
    const f = 90 * Math.exp(-t * 6) + 40;
    sfx[i0 + i] += Math.sin(2 * Math.PI * f * t) * Math.exp(-t * 3) * 0.7;
    sfx[i0 + i] += rnd() * Math.exp(-t * 25) * 0.3; // impacto
  }
  for (const n of [74, 81, 86]) addTone(sfx, at + 0.02, 1.5, noteHz(n), 0.12, { wave: "sine", a: 0.01, d: 0.4, s: 0.3, r: 0.8 });
}

// Transiciones de placa (frames 60/120/180/240 a 30 fps → 2,4,6,8 s)
for (const t of [2, 4, 6, 8]) whoosh(t - 0.18);
// Gancho (placa 1)
pop(0.25, 700); pop(0.55, 900); pop(0.85, 1100);
// Placas 2-4: etiqueta, título, cuerpo
for (const base of [2, 4, 6]) {
  pop(base + 0.15, 1200, 0.35);
  pop(base + 0.42, 800, 0.5);
  pop(base + 0.75, 650, 0.35);
}
// Cierre
hit(8.1);
pop(8.65, 1000, 0.45);

// ---------- MEZCLA ----------
const mix = mk();
for (let i = 0; i < N; i++) mix[i] = clamp(music[i] * 0.55 + sfx[i] * 1.0);

function writeWav(path, data) {
  const buf = Buffer.alloc(44 + data.length * 2);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + data.length * 2, 4); buf.write("WAVE", 8);
  buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write("data", 36); buf.writeUInt32LE(data.length * 2, 40);
  for (let i = 0; i < data.length; i++) buf.writeInt16LE(Math.round(clamp(data[i]) * 32767), 44 + i * 2);
  writeFileSync(path, buf);
}
mkdirSync("public/audio", { recursive: true });
writeWav("public/audio/music.wav", music);
writeWav("public/audio/sfx.wav", sfx);
writeWav("public/audio/mix.wav", mix);
console.log("ok: music.wav, sfx.wav, mix.wav (10 s, 48 kHz)");
