// this_file: src/index.ts

import { GEO, COMMON } from "./wordlist.js";
import { mangle, mulberry32, joinClean } from "./mangle.js";

export interface NamzyOptions {
  online?: boolean;
  seed?: number;
}

function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function pick<T>(arr: T[], rng: () => number): T {
  return arr[Math.floor(rng() * arr.length)];
}

async function fetchOnlineWords(): Promise<string[]> {
  const url = `https://random-word-api.herokuapp.com/word?number=2&length=6`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const data = (await resp.json()) as string[];
  if (!Array.isArray(data) || data.length < 2) throw new Error("Bad response");
  return data.slice(0, 2).map((w) => w.toLowerCase().replace(/[^a-z]/g, ""));
}

/**
 * Generate a single fused, mangled namzy name.
 * Two raw words → junction-cleaned fusion → consonant rotation → capitalize.
 */
export async function generate(opts?: NamzyOptions): Promise<string> {
  const online = opts?.online ?? false;
  const seed = opts?.seed ?? Date.now();
  const rng = mulberry32(seed);

  let w1: string;
  let w2: string;

  if (online) {
    try {
      const words = await fetchOnlineWords();
      [w1, w2] = words;
    } catch {
      w1 = pick(GEO, rng).toLowerCase();
      w2 = pick(COMMON, rng).toLowerCase();
    }
  } else {
    w1 = pick(GEO, rng).toLowerCase();
    w2 = pick(COMMON, rng).toLowerCase();
  }

  const fused = joinClean(w1, w2);
  return capitalize(mangle(fused));
}

export { mangle, joinClean, mulberry32 };
export { GEO, COMMON } from "./wordlist.js";
