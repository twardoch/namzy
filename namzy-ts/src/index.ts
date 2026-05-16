// this_file: src/index.ts

import { activeRotationMask, joinClean, mangle, mulberry32 } from "./mangle.js";
import { COMMON, GEO } from "./wordlist.js";

export interface NamzyOptions {
	seed?: number;
}

function capitalize(s: string): string {
	return s.charAt(0).toUpperCase() + s.slice(1);
}

function pick<T>(arr: T[], rng: () => number): T {
	return arr[Math.floor(rng() * arr.length)];
}

/**
 * Generate a single fused, mangled namzy name.
 * Two raw words → junction-cleaned fusion → consonant rotation → capitalize.
 */
export async function generate(opts?: NamzyOptions): Promise<string> {
	const seed = opts?.seed ?? Date.now();
	const rng = mulberry32(seed);

	const w1 = pick(GEO, rng).toLowerCase();
	const w2 = pick(COMMON, rng).toLowerCase();
	const [first, second] = rng() < 0.5 ? [w1, w2] : [w2, w1];

	const fused = joinClean(first, second);
	return capitalize(mangle(fused, activeRotationMask(rng)));
}

export { COMMON, GEO } from "./wordlist.js";
export { activeRotationMask, joinClean, mangle, mulberry32 };
