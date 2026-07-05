// this_file: namzy-ts/test/namzy.test.ts
// Contract tests: determinism and output shape for the TypeScript reference impl.
// Run with: npm test

import assert from "node:assert/strict";
import { test } from "node:test";

import { applyRotation, generate, generateMany, mulberry32 } from "../src/index.js";
import { BAD_SEAMS, ROTATIONS, STEMS } from "../src/wordlist.js";

test("generate is deterministic for a seed", () => {
  assert.equal(generate({ seed: 42 }), generate({ seed: 42 }));
});

test("names are capitalized, ASCII, and short", () => {
  for (let seed = 0; seed < 500; seed++) {
    const name = generate({ seed });
    assert.ok(name.length > 0, "name must not be empty");
    assert.match(name[0], /[A-Z]/, `not capitalized: ${name}`);
    assert.match(name, /^[A-Za-z]+$/, `non-ascii: ${name}`);
    assert.ok(name.length <= 16, `unexpectedly long: ${name}`);
  }
});

test("different seeds usually differ", () => {
  const names = new Set<string>();
  for (let seed = 0; seed < 200; seed++) names.add(generate({ seed }));
  assert.ok(names.size > 150, `too few distinct names: ${names.size}`);
});

test("generateMany returns the requested count deterministically", () => {
  const first = generateMany(25, { seed: 7 });
  assert.equal(first.length, 25);
  assert.deepEqual(first, generateMany(25, { seed: 7 }));
});

test("data tables are well-formed", () => {
  assert.ok(STEMS.length > 0);
  assert.ok(ROTATIONS.length > 0);
  assert.ok(BAD_SEAMS.length > 0);
  for (const stem of STEMS) assert.match(stem, /^[a-z]+$/, `bad stem: ${stem}`);
  for (const [src, dst] of ROTATIONS) {
    assert.ok(src.length > 0 && dst.length > 0);
    assert.notEqual(src, dst, `no-op rotation: ${src}`);
  }
});

test("applyRotation leaves a pure-vowel string untouched", () => {
  // Every rotation source starts with a consonant.
  assert.ok(ROTATIONS.every(([src]) => !"aeiouy".includes(src[0])));
  assert.equal(applyRotation("aeiou", mulberry32(0)), "aeiou");
});
