import assert from "node:assert";
import {
  isAudioMuted,
  setAudioMuted,
  toggleAudioMute,
  subscribeAudioMute,
  isReducedMotionPreferred,
} from "./audio";

// Mock minimal browser environment
globalThis.window = {
  matchMedia: (query: string) => ({
    matches: query.includes("prefers-reduced-motion"),
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  }),
  AudioContext: class MockAudioContext {
    state = "running";
    currentTime = 0;
    sampleRate = 44100;
    destination = {};
    createBuffer(channels: number, length: number, sampleRate: number) {
      return {
        getChannelData: () => new Float32Array(length),
        length,
        sampleRate,
      };
    }
    createBufferSource() {
      return {
        buffer: null,
        connect: () => {},
        disconnect: () => {},
        start: () => {},
        stop: () => {},
      };
    }
    createBiquadFilter() {
      return {
        type: "bandpass",
        frequency: { setValueAtTime: () => {} },
        Q: { setValueAtTime: () => {} },
        connect: () => {},
        disconnect: () => {},
      };
    }
    createGain() {
      return {
        gain: {
          setValueAtTime: () => {},
          exponentialRampToValueAtTime: () => {},
        },
        connect: () => {},
        disconnect: () => {},
      };
    }
    createOscillator() {
      return {
        type: "sine",
        frequency: {
          setValueAtTime: () => {},
          exponentialRampToValueAtTime: () => {},
        },
        connect: () => {},
        disconnect: () => {},
        start: () => {},
        stop: () => {},
      };
    }
    resume() {
      return Promise.resolve();
    }
  } as unknown as typeof AudioContext,
} as unknown as Window & typeof globalThis;

const storage = new Map<string, string>();
globalThis.localStorage = {
  getItem: (key: string) => storage.get(key) ?? null,
  setItem: (key: string, val: string) => {
    storage.set(key, val);
  },
  removeItem: (key: string) => {
    storage.delete(key);
  },
  clear: () => storage.clear(),
  key: () => null,
  length: 0,
};

// 1. Check reduced motion detection
assert.strictEqual(isReducedMotionPreferred(), true);

// 2. Default mute state should honor prefers-reduced-motion when no localStorage override
storage.clear();
assert.strictEqual(isAudioMuted(), true);

// 3. Explicit unmute override
setAudioMuted(false);
assert.strictEqual(isAudioMuted(), false);
assert.strictEqual(storage.get("aegis_audio_muted"), "false");

// 4. Toggle mute
const toggled = toggleAudioMute();
assert.strictEqual(toggled, true);
assert.strictEqual(isAudioMuted(), true);

// 5. Subscription notification
let notifiedValue: boolean | null = null;
const unsub = subscribeAudioMute((muted) => {
  notifiedValue = muted;
});
assert.strictEqual(notifiedValue, true);

setAudioMuted(false);
assert.strictEqual(notifiedValue, false);
unsub();

setAudioMuted(true);
// Should not update after unsubscribe
assert.strictEqual(notifiedValue, false);

console.log("ALL AUDIO TESTS PASSED");
