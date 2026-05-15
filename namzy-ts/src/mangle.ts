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

const ROTATION: Record<string, string> = {
  c: "q", f: "v", k: "c", q: "k",
  s: "z", z: "s", v: "f", w: "u",
};

/** Consonant rotation: c→q, f→v, k→c, q→k, s→z, z→s, v→f, w→u. Case-preserving. */
export function mangle(s: string): string {
  let out = "";
  for (const ch of s) {
    const lower = ch.toLowerCase();
    const repl = ROTATION[lower];
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
  let head = a;
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
