## Objective

`namzy` is a family of equivalent algorithms in TypeScript (`namzy-ts`), Python (`namzy-py`), C++ Qt5 (`namzy-cpp`), and Rust (`namzy-rs`) that generate fun, unique, human-friendly project names.

## Contract

Every name is a single fused token that *looks* like one word but is two words spliced together and then mangled:

1. **Always two-words-fused.** Pick word 1 + word 2 from the vocabulary, lowercase both.
2. **Junction cleanup at the seam.** Up to two passes:
   - if `last(word1) == first(word2)` → drop `first(word2)`
   - else if both are vowels (`a e i o u y`) → drop `first(word2)`
3. **Concatenate** without separator.
4. **Consonant rotation** (case-preserving), applied per letter:
   `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u`
5. **Capitalize first letter only.**

Each implementation is seeded by the current timestamp (or a caller-supplied integer). Vocabulary uses basic `A–Za–z` only — geographic names + common Latin-alphabet words.

Two operating modes are required:

- **Self-contained** — bundled wordlist, no network.
- **Online** — fetches from a public no-auth API; falls back to bundled on failure.

The implementations do not need to produce identical output across languages. Keep the code simple.

## Deliverables

Each implementation in a sibling subfolder, publishable as its ecosystem's package (npm / PyPI / crates.io; C++ ships binary only). Top-level `README.md`, `LICENSE` (MIT), `docs/index.html` demo built from the TS implementation, plus `build.sh` and `publish.sh` orchestrating the lot.
