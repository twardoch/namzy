// this_file: src/mangle.ts

import { BAD_SEAMS, ROTATIONS, STEMS } from "./wordlist.js";

const MAX_LEN = 12;
const MAX_TRIES = 8;

export function mulberry32(seed: number): () => number {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function pick<T>(arr: readonly T[], rng: () => number): T {
  return arr[Math.floor(rng() * arr.length)];
}

function hasTripleLetter(s: string): boolean {
  for (let i = 2; i < s.length; i++) {
    if (s[i] === s[i - 1] && s[i] === s[i - 2]) return true;
  }
  return false;
}

function junctionUgly(compound: string, junction: number): boolean {
  // Inspect the 4-char window centered on the junction.
  const start = Math.max(0, junction - 2);
  const end = Math.min(compound.length, junction + 2);
  const win = compound.slice(start, end);
  for (const seam of BAD_SEAMS) {
    if (win.includes(seam)) return true;
  }
  return false;
}

/** Apply one rotation at a randomly chosen matching position. */
export function applyRotation(s: string, rng: () => number): string {
  type Match = { i: number; src: string; dst: string };
  const matches: Match[] = [];
  for (let i = 0; i < s.length; i++) {
    for (const [src, dst] of ROTATIONS) {
      if (s.slice(i, i + src.length) === src) {
        matches.push({ i, src, dst });
      }
    }
  }
  if (matches.length === 0) return s;
  const m = matches[Math.floor(rng() * matches.length)];
  return s.slice(0, m.i) + m.dst + s.slice(m.i + m.src.length);
}

function capitalize(s: string): string {
  return s.length === 0 ? s : s[0].toUpperCase() + s.slice(1);
}

/** Build one name with junction validation + one rotation. */
export function buildName(rng: () => number): string {
  let best = "";
  for (let attempt = 0; attempt < MAX_TRIES; attempt++) {
    const a = pick(STEMS, rng);
    const b = pick(STEMS, rng);
    const compound = a + b;
    if (compound.length > MAX_LEN) {
      best = best || compound;
      continue;
    }
    if (hasTripleLetter(compound)) {
      best = best || compound;
      continue;
    }
    if (junctionUgly(compound, a.length)) {
      best = best || compound;
      continue;
    }
    return capitalize(applyRotation(compound, rng));
  }
  // All attempts had some flaw; rotate and ship the first candidate anyway.
  return capitalize(applyRotation(best, rng));
}
