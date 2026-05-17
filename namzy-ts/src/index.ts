// this_file: src/index.ts

import { applyRotations, buildName, mulberry32 } from "./mangle.js";
import { ROTATIONS, STEMS } from "./wordlist.js";

export interface NamzyOptions {
  seed?: number;
}

/** Generate one namzy name. Default seed is the current timestamp. */
export function generate(opts?: NamzyOptions): string {
  const seed = opts?.seed ?? Date.now();
  return buildName(mulberry32(seed));
}

/** Generate `count` names. Distinct seeds derived from the base seed. */
export function generateMany(count: number, opts?: NamzyOptions): string[] {
  const base = opts?.seed ?? Date.now();
  const out: string[] = [];
  for (let i = 0; i < count; i++) {
    out.push(generate({ seed: base + i * 2654435761 }));
  }
  return out;
}

export { STEMS, ROTATIONS } from "./wordlist.js";
export { applyRotations, buildName, mulberry32 };
