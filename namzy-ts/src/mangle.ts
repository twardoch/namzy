// this_file: src/mangle.ts

/** Simple seeded mulberry32 RNG — returns a function that yields [0,1) floats */
export function mulberry32(seed: number): () => number {
  let s = seed >>> 0;
  return () => {
    s += 0x6d2b79f5;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

type RotationRule = readonly [from: string, to: string];

export const ROTATION_RULES: readonly RotationRule[] = [
  ["c", "q"],
  ["f", "v"],
  ["k", "c"],
  ["q", "k"],
  ["s", "z"],
  ["z", "s"],
  ["v", "f"],
  ["w", "u"],
  ["b", "p"],
  ["p", "b"],
];

const ALL_ROTATIONS = (1 << ROTATION_RULES.length) - 1;

function rotationFor(lower: string, activeMask: number): string | undefined {
  for (let i = 0; i < ROTATION_RULES.length; i++) {
    if ((activeMask & (1 << i)) === 0) {
      continue;
    }
    const [from, to] = ROTATION_RULES[i];
    if (lower === from) {
      return to;
    }
  }
  return undefined;
}

/** Choose 1..10 active consonant-rotation rules from the seeded RNG. */
export function activeRotationMask(rng: () => number): number {
  const order = ROTATION_RULES.map((_, i) => i);
  const activeCount = 1 + Math.floor(rng() * ROTATION_RULES.length);
  for (let i = 0; i < activeCount; i++) {
    const swap = i + Math.floor(rng() * (order.length - i));
    [order[i], order[swap]] = [order[swap], order[i]];
  }
  return order.slice(0, activeCount).reduce((mask, i) => mask | (1 << i), 0);
}

/** Consonant rotation. Case-preserving. Defaults to all rules for direct helper use. */
export function mangle(s: string, activeMask = ALL_ROTATIONS): string {
  let out = "";
  for (const ch of s) {
    const lower = ch.toLowerCase();
    const repl = rotationFor(lower, activeMask);
    if (repl === undefined) {
      out += ch;
    } else {
      out += ch === lower ? repl : repl.toUpperCase();
    }
  }
  return out;
}

const VOWELS = new Set(["a", "e", "i", "o", "u", "y"]);

/**
 * Fuse two lowercase words at a clean junction.
 * Drops the first char of `b` while it duplicates the tail of `a`,
 * or while the seam is vowel-vowel. Max two trims.
 */
export function joinClean(a: string, b: string): string {
  const head = a;
  let tail = b;
  for (let i = 0; i < 2 && head.length > 0 && tail.length > 0; i++) {
    const last = head[head.length - 1].toLowerCase();
    const first = tail[0].toLowerCase();
    if (last === first) {
      tail = tail.slice(1);
    } else if (VOWELS.has(last) && VOWELS.has(first)) {
      tail = tail.slice(1);
    } else {
      break;
    }
  }
  return head + tail;
}
