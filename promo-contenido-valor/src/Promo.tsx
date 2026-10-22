import {
  AbsoluteFill,
  Audio,
  Easing,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CameraMotionBlur } from "@remotion/motion-blur";
import { COLORS, CTA, FONTS, HANDLE, HOOK, POSTS, Post } from "./brand";

// ---------- helpers ----------
const SAFE_X = 96; // margen lateral (zona segura Reels)
const SAFE_TOP = 260;
const SAFE_BOTTOM = 380;

const usePop = (
  delay: number,
  opts?: { damping?: number; stiffness?: number },
) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({
    frame: frame - delay,
    fps,
    config: {
      damping: opts?.damping ?? 14,
      stiffness: opts?.stiffness ?? 160,
      mass: 0.8,
    },
  });
};

// Fondo: navy con gradiente + "ticker" de líneas doradas que se desplaza lento
const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 300], [0, -120]);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 80% at 50% 0%, ${COLORS.navy} 0%, ${COLORS.navyDeep} 70%)`,
        overflow: "hidden",
      }}
    >
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: -200,
            right: -200,
            top: 300 + i * 260 + drift,
            height: 2,
            background: COLORS.gold,
            opacity: 0.08,
            transform: "rotate(-8deg)",
          }}
        />
      ))}
      {/* barra lateral dorada fija: identidad */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: 14,
          background: COLORS.gold,
        }}
      />
    </AbsoluteFill>
  );
};

// Transición: barra dorada que barre la pantalla (whoosh) en los últimos frames de cada placa
const Wipe: React.FC<{ at: number }> = ({ at }) => {
  const frame = useCurrentFrame();
  const t = frame - at;
  if (t < -6 || t > 10) return null;
  const x = interpolate(t, [-6, 10], [-1200, 1200], {
    easing: Easing.inOut(Easing.cubic),
  });
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          width: 260,
          left: 540 + x - 130,
          background: COLORS.gold,
          transform: "skewX(-14deg)",
          boxShadow: `0 0 80px ${COLORS.gold}`,
        }}
      />
    </AbsoluteFill>
  );
};

// Entrada/salida de cada placa: slide + fade
const SceneWrap: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const inP = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const outP = interpolate(
    frame,
    [durationInFrames - 8, durationInFrames],
    [1, 0],
    {
      extrapolateLeft: "clamp",
      easing: Easing.in(Easing.cubic),
    },
  );
  const y = (1 - inP) * 40 - (1 - outP) * 40;
  return (
    <AbsoluteFill
      style={{ opacity: Math.min(inP, outP), transform: `translateY(${y}px)` }}
    >
      {children}
    </AbsoluteFill>
  );
};

const Chip: React.FC<{ children: React.ReactNode; delay: number }> = ({
  children,
  delay,
}) => {
  const p = usePop(delay);
  return (
    <div
      style={{
        display: "inline-block",
        fontFamily: FONTS.body,
        fontWeight: 600,
        fontSize: 34,
        letterSpacing: 6,
        textTransform: "uppercase",
        color: COLORS.navyDeep,
        background: COLORS.gold,
        padding: "14px 28px",
        transform: `scale(${p})`,
        transformOrigin: "left center",
        opacity: p,
      }}
    >
      {children}
    </div>
  );
};

// Logo placeholder: monograma MT en círculo dorado + handle
const Logo: React.FC<{ scale?: number }> = ({ scale = 1 }) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 28 * scale,
    }}
  >
    <div
      style={{
        width: 260 * scale,
        height: 260 * scale,
        borderRadius: "50%",
        background: COLORS.gold,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: FONTS.display,
        fontWeight: 800,
        fontSize: 118 * scale,
        color: COLORS.navyDeep,
        letterSpacing: -4 * scale,
        boxShadow: `0 0 120px rgba(212,169,71,0.45)`,
      }}
    >
      MT
    </div>
  </div>
);

// ---------- PLACA 1: gancho ----------
const Hook: React.FC = () => {
  const lines = [HOOK.top, HOOK.mid, HOOK.bottom];
  const delays = [6, 15, 24]; // sincronizado con pops a 0.25 / 0.55 / 0.85 s (aprox.)
  return (
    <SceneWrap>
      <div
        style={{
          position: "absolute",
          left: SAFE_X,
          right: SAFE_X,
          top: SAFE_TOP + 120,
          display: "flex",
          flexDirection: "column",
          gap: 10,
        }}
      >
        <Chip delay={2}>Contenido de valor</Chip>
        <div style={{ height: 40 }} />
        {lines.map((l, i) => (
          <HookLine key={l} text={l} delay={delays[i]} accent={i === 1} />
        ))}
      </div>
      <div
        style={{
          position: "absolute",
          bottom: SAFE_BOTTOM,
          left: SAFE_X,
          fontFamily: FONTS.body,
          fontWeight: 500,
          fontSize: 40,
          color: COLORS.muted,
        }}
      >
        {HANDLE}
      </div>
    </SceneWrap>
  );
};

const HookLine: React.FC<{ text: string; delay: number; accent?: boolean }> = ({
  text,
  delay,
  accent,
}) => {
  const p = usePop(delay, { damping: 16, stiffness: 190 });
  return (
    <div
      style={{
        fontFamily: FONTS.display,
        fontWeight: 800,
        fontSize: 132,
        lineHeight: 1.02,
        letterSpacing: -4,
        color: accent ? COLORS.gold : COLORS.offWhite,
        transform: `translateY(${(1 - p) * 60}px) scale(${0.9 + p * 0.1})`,
        opacity: p,
        transformOrigin: "left center",
      }}
    >
      {text}
    </div>
  );
};

// ---------- PLACAS 2-4: publicación ----------
const PostCard: React.FC<{ post: Post; index: number }> = ({ post, index }) => {
  const pLabel = usePop(4);
  const pTitle = usePop(12, { damping: 16, stiffness: 180 });
  const pBody = usePop(22);
  const frame = useCurrentFrame();
  const bar = interpolate(frame, [12, 40], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <SceneWrap>
      {/* número grande de fondo */}
      <div
        style={{
          position: "absolute",
          right: SAFE_X - 30,
          top: SAFE_TOP - 80,
          fontFamily: FONTS.display,
          fontWeight: 800,
          fontSize: 420,
          color: COLORS.gold,
          opacity: 0.1 * pLabel,
          lineHeight: 1,
          letterSpacing: -20,
        }}
      >
        {String(index + 1).padStart(2, "0")}
      </div>
      <div
        style={{
          position: "absolute",
          left: SAFE_X,
          right: SAFE_X,
          top: SAFE_TOP + 160,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            opacity: pLabel,
            transform: `translateX(${(1 - pLabel) * -40}px)`,
          }}
        >
          <Chip delay={4}>{post.label}</Chip>
        </div>
        <div style={{ height: 56 }} />
        <div
          style={{
            fontFamily: FONTS.display,
            fontWeight: 800,
            fontSize: 108,
            lineHeight: 1.04,
            letterSpacing: -3,
            color: COLORS.offWhite,
            opacity: pTitle,
            transform: `translateY(${(1 - pTitle) * 50}px)`,
          }}
        >
          {post.title}
        </div>
        <div
          style={{
            marginTop: 40,
            height: 8,
            width: 360 * bar,
            background: COLORS.gold,
          }}
        />
        <div
          style={{
            marginTop: 40,
            fontFamily: FONTS.body,
            fontWeight: 500,
            fontSize: 58,
            lineHeight: 1.25,
            color: COLORS.muted,
            opacity: pBody,
            transform: `translateY(${(1 - pBody) * 30}px)`,
          }}
        >
          {post.body}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          bottom: SAFE_BOTTOM,
          left: SAFE_X,
          fontFamily: FONTS.body,
          fontWeight: 500,
          fontSize: 40,
          color: COLORS.muted,
        }}
      >
        {HANDLE}
      </div>
    </SceneWrap>
  );
};

// ---------- PLACA 5: cierre ----------
const Outro: React.FC = () => {
  const pLogo = usePop(3, { damping: 12, stiffness: 140 });
  const pCta = usePop(18);
  const frame = useCurrentFrame();
  const glow = 0.5 + 0.5 * Math.sin(frame / 6);
  return (
    <SceneWrap>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: SAFE_TOP + 120,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 70,
        }}
      >
        <div style={{ transform: `scale(${pLogo})`, opacity: pLogo }}>
          <Logo />
        </div>
        <div
          style={{
            opacity: pCta,
            transform: `translateY(${(1 - pCta) * 40}px)`,
            textAlign: "center",
            paddingLeft: SAFE_X,
            paddingRight: SAFE_X,
          }}
        >
          <div
            style={{
              fontFamily: FONTS.display,
              fontWeight: 800,
              fontSize: 96,
              color: COLORS.offWhite,
              letterSpacing: -2,
              lineHeight: 1.05,
            }}
          >
            {CTA.line1}{" "}
            <span
              style={{
                color: COLORS.gold,
                textShadow: `0 0 ${30 * glow}px rgba(212,169,71,0.6)`,
              }}
            >
              {HANDLE}
            </span>
          </div>
          <div
            style={{
              marginTop: 28,
              fontFamily: FONTS.body,
              fontWeight: 500,
              fontSize: 54,
              color: COLORS.muted,
              lineHeight: 1.2,
            }}
          >
            {CTA.line2}
          </div>
        </div>
      </div>
    </SceneWrap>
  );
};

// ---------- composición ----------
export const SCENE = 60; // 2 s a 30 fps

export const Promo: React.FC = () => {
  return (
    <AbsoluteFill>
      {/* Motion blur de cámara: 10 muestras por frame, obturador 180° */}
      <CameraMotionBlur samples={10} shutterAngle={180}>
        <Background />
        <Sequence from={0} durationInFrames={SCENE}>
          <Hook />
        </Sequence>
        {POSTS.map((p, i) => (
          <Sequence
            key={p.label}
            from={SCENE * (i + 1)}
            durationInFrames={SCENE}
          >
            <PostCard post={p} index={i} />
          </Sequence>
        ))}
        <Sequence from={SCENE * 4} durationInFrames={SCENE}>
          <Outro />
        </Sequence>
        {[1, 2, 3, 4].map((k) => (
          <Wipe key={k} at={SCENE * k} />
        ))}
      </CameraMotionBlur>
      <Audio src={staticFile("audio/mix.wav")} />
    </AbsoluteFill>
  );
};
