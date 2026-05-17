// this_file: src/mangle.ts

import { ROTATIONS, STEMS } from "./wordlist.js";

/** Seeded mulberry32 RNG — yields [0,1) floats. */
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

const ROT_MAP = new Map<string, string>(ROTATIONS as readonly (readonly [string, string])[]);

function rotateAt(s: string, pos: number): string {
  const ch = s[pos];
  const lower = ch.toLowerCase();
  const repl = ROT_MAP.get(lower);
  if (repl === undefined) return s;
  const out = ch === lower ? repl : repl.toUpperCase();
  return s.slice(0, pos) + out + s.slice(pos + 1);
}

/** Apply 1 or 2 rotations on randomly selected positions of the compound. */
export function applyRotations(compound: string, rng: () => number): string {
  if (compound.length === 0) return compound;
  const passes = rng() < 0.5 ? 1 : 2;
  let out = compound;
  for (let i = 0; i < passes; i++) {
    out = rotateAt(out, Math.floor(rng() * out.length));
  }
  return out;
}

function capitalize(s: string): string {
  return s.length === 0 ? s : s[0].toUpperCase() + s.slice(1);
}

/** Build one name: any two stems, concatenated, lightly rotated, capitalized. */
export function buildName(rng: () => number): string {
  const a = pick(STEMS, rng);
  const b = pick(STEMS, rng);
  return capitalize(applyRotations(a + b, rng));
}
