/**
 * Aegis-JKN Web Audio API Procedural Sound Engine
 * Sesuai panduan UI/UX userinterface-wiki (Rule 5 & 6):
 * - Sintesis prosedural tanpa file audio eksternal
 * - Singleton AudioContext dengan auto-resume
 * - Filtered noise burst untuk klik (5-15ms, 4000Hz bandpass)
 * - Tonal oscillators dengan pitch movement untuk notifikasi sukses & peringatan
 * - Exponential decay dengan target non-zero (0.001)
 * - Pembersihan audio nodes (cleanup onended)
 * - Mute toggle tersimpan di localStorage + menghormati prefers-reduced-motion
 */

declare global {
  interface Window {
    webkitAudioContext?: typeof AudioContext;
  }
}

let sharedContext: AudioContext | null = null;

function getAudioContext(): AudioContext | null {
  if (typeof window === "undefined") return null;
  if (!sharedContext) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (AudioCtx) {
      sharedContext = new AudioCtx();
    }
  }
  if (sharedContext && sharedContext.state === "suspended") {
    sharedContext.resume().catch(() => {});
  }
  return sharedContext;
}

/**
 * Deteksi preferensi reduced motion dari sistem operasi pengguna
 */
export function isReducedMotionPreferred(): boolean {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

// Key penyimpanan status bisukan suara di localStorage
const STORAGE_KEY = "aegis_audio_muted";

type AudioMuteListener = (muted: boolean) => void;
const listeners = new Set<AudioMuteListener>();

/**
 * Status mute audio saat ini
 */
export function isAudioMuted(): boolean {
  if (typeof window === "undefined") return true;

  // Jika sistem meminta reduced motion, default bisukan audio demi aksesibilitas
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored !== null) {
    return stored === "true";
  }
  return isReducedMotionPreferred();
}

/**
 * Atur status mute audio secara manual
 */
export function setAudioMuted(muted: boolean): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, muted ? "true" : "false");
  listeners.forEach((fn) => {
    try {
      fn(muted);
    } catch (e) {
      console.error("Audio listener error:", e);
    }
  });
}

/**
 * Toggle status mute audio
 */
export function toggleAudioMute(): boolean {
  const next = !isAudioMuted();
  setAudioMuted(next);
  if (!next) {
    // Berikan feedback subtle saat mengaktifkan suara
    playSubtleClick();
  }
  return next;
}

/**
 * Berlangganan perubahan status mute audio
 */
export function subscribeAudioMute(fn: AudioMuteListener): () => void {
  listeners.add(fn);
  fn(isAudioMuted());
  return () => {
    listeners.delete(fn);
  };
}

/**
 * Suara klik lembut prosedural (5-15ms, 4000Hz bandpass filter)
 * Digunakan untuk interaksi tombol & seleksi
 */
export function playSubtleClick(): void {
  if (isAudioMuted()) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const durationSec = 0.009; // 9ms (dalam rentang 5-15ms)
  const bufferSize = Math.max(1, Math.floor(ctx.sampleRate * durationSec));
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  // Filtered decaying noise burst
  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.35));
  }

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const filter = ctx.createBiquadFilter();
  filter.type = "bandpass";
  filter.frequency.setValueAtTime(4000, ctx.currentTime);
  filter.Q.setValueAtTime(3.2, ctx.currentTime);

  const gain = ctx.createGain();
  const t = ctx.currentTime;
  gain.gain.setValueAtTime(0.08, t);
  gain.gain.exponentialRampToValueAtTime(0.001, t + durationSec);

  source.connect(filter);
  filter.connect(gain);
  gain.connect(ctx.destination);

  source.onended = () => {
    source.disconnect();
    filter.disconnect();
    gain.disconnect();
  };

  source.start(t);
}

/**
 * Suara lonceng keberhasilan (Success chime)
 * Harmoni dua nada (E5 659Hz -> A5 880Hz) yang naik dengan peluruhan alami
 * Diputar saat verifikator menyetujui (Approve) klaim
 */
export function playSuccessChime(): void {
  if (isAudioMuted()) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const t = ctx.currentTime;
  const masterGain = ctx.createGain();
  masterGain.gain.setValueAtTime(0.12, t);
  masterGain.connect(ctx.destination);

  // Tone 1: E5 (659.25 Hz)
  const osc1 = ctx.createOscillator();
  const gain1 = ctx.createGain();
  osc1.type = "sine";
  osc1.frequency.setValueAtTime(659.25, t);
  osc1.frequency.exponentialRampToValueAtTime(665, t + 0.08);

  gain1.gain.setValueAtTime(0.12, t);
  gain1.gain.exponentialRampToValueAtTime(0.001, t + 0.16);

  osc1.connect(gain1);
  gain1.connect(masterGain);

  // Tone 2: A5 (880.00 Hz) - masuk sedikit setelah nada pertama untuk efek arpeggio lembut
  const osc2 = ctx.createOscillator();
  const gain2 = ctx.createGain();
  osc2.type = "triangle";
  osc2.frequency.setValueAtTime(880, t + 0.05);

  gain2.gain.setValueAtTime(0.001, t);
  gain2.gain.setValueAtTime(0.14, t + 0.05);
  gain2.gain.exponentialRampToValueAtTime(0.001, t + 0.24);

  osc2.connect(gain2);
  gain2.connect(masterGain);

  osc1.start(t);
  osc1.stop(t + 0.17);

  osc2.start(t + 0.05);
  osc2.stop(t + 0.25);

  osc2.onended = () => {
    osc1.disconnect();
    osc2.disconnect();
    gain1.disconnect();
    gain2.disconnect();
    masterGain.disconnect();
  };
}

/**
 * Suara peringatan waspada (Warning alert)
 * Nada ganda turun non-punishing (494Hz -> 392Hz) dengan filter lembut
 * Diputar saat verifikator mengeksekusi Tolak / Eskalasi ke P2PK
 */
export function playWarningAlert(): void {
  if (isAudioMuted()) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const t = ctx.currentTime;
  const masterGain = ctx.createGain();
  masterGain.gain.setValueAtTime(0.12, t);

  // Lowpass filter untuk memastikan nada peringatan tidak menusuk telinga
  const filter = ctx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.setValueAtTime(1400, t);

  filter.connect(ctx.destination);
  masterGain.connect(filter);

  // Tone 1: B4 (493.88 Hz) turun perlahan
  const osc1 = ctx.createOscillator();
  const gain1 = ctx.createGain();
  osc1.type = "triangle";
  osc1.frequency.setValueAtTime(493.88, t);
  osc1.frequency.exponentialRampToValueAtTime(440, t + 0.07);

  gain1.gain.setValueAtTime(0.12, t);
  gain1.gain.exponentialRampToValueAtTime(0.001, t + 0.11);

  osc1.connect(gain1);
  gain1.connect(masterGain);

  // Tone 2: G4 (392.00 Hz) nada resolusi peringatan
  const osc2 = ctx.createOscillator();
  const gain2 = ctx.createGain();
  osc2.type = "sine";
  osc2.frequency.setValueAtTime(392, t + 0.06);

  gain2.gain.setValueAtTime(0.001, t);
  gain2.gain.setValueAtTime(0.14, t + 0.06);
  gain2.gain.exponentialRampToValueAtTime(0.001, t + 0.22);

  osc2.connect(gain2);
  gain2.connect(masterGain);

  osc1.start(t);
  osc1.stop(t + 0.12);

  osc2.start(t + 0.06);
  osc2.stop(t + 0.23);

  osc2.onended = () => {
    osc1.disconnect();
    osc2.disconnect();
    gain1.disconnect();
    gain2.disconnect();
    masterGain.disconnect();
    filter.disconnect();
  };
}

/**
 * Suara konfirmasi permintaan klarifikasi (Clarify RS)
 * Dua ketukan netral bernada santai
 */
export function playClarifyChime(): void {
  if (isAudioMuted()) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const t = ctx.currentTime;
  const masterGain = ctx.createGain();
  masterGain.gain.setValueAtTime(0.1, t);
  masterGain.connect(ctx.destination);

  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = "sine";
  osc.frequency.setValueAtTime(523.25, t); // C5
  osc.frequency.setValueAtTime(587.33, t + 0.07); // D5

  gain.gain.setValueAtTime(0.1, t);
  gain.gain.exponentialRampToValueAtTime(0.001, t + 0.18);

  osc.connect(gain);
  gain.connect(masterGain);

  osc.start(t);
  osc.stop(t + 0.19);

  osc.onended = () => {
    osc.disconnect();
    gain.disconnect();
    masterGain.disconnect();
  };
}

/**
 * Helper untuk memutar suara berdasarkan tipe aksi HITL
 */
export function playActionAudio(action: "APPROVE" | "CLARIFY_RS" | "ESCALATE_P2PK"): void {
  switch (action) {
    case "APPROVE":
      playSuccessChime();
      break;
    case "ESCALATE_P2PK":
      playWarningAlert();
      break;
    case "CLARIFY_RS":
      playClarifyChime();
      break;
  }
}
