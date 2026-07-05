# namzy

`namzy` generates fun, human-friendly project names for software or typefaces. It fuses two short words from a bundled vocabulary into a single token, rejects ugly seams, and nudges one syllable so the result looks invented but stays pronounceable — e.g. `Pillarson`, `Hazeldovir`, `Omorthames`, `Crispogra`.

A live demo lives in [`docs/index.md`](./docs/index.md) (also browsable via GitHub Pages once enabled).

```bash
pip install namzy && namzy --count 5      # Python
npx @twardoch/namzy --count 5             # TypeScript
cargo install namzy && namzy --count 5    # Rust
```

## Visual

<img src="docs/assets/icon.png" alt="A signpost whose two arrows fuse into one, half in daylight and half in moonlight — two words joined into a single place." width="180">

Two arrows fused into one signpost: two words joined into a single place.

## Repository layout

Four sibling packages, one per language, each independently publishable:

| Folder       | Language        | Publishes to |
|--------------|-----------------|--------------|
| `namzy-ts/`  | TypeScript      | npm          |
| `namzy-py/`  | Python          | PyPI         |
| `namzy-rs/`  | Rust            | crates.io    |
| `namzy-cpp/` | C++ (Qt5)       | (not published) |

The implementations are siblings, not a monorepo with shared code. Each follows its own ecosystem's conventions.

## Shared contract

All four implementations run the same four steps:

1. **Two stems → one fused token.** Pick two stems at random and concatenate them. Stems are hand-curated across 12 discipline packs (cities, rivers, colors, adjectives, nouns, verbs, names, trees, birds, gems, weather, myth), each `≤2` syllables and `≤7` characters. The bundled, deduplicated list holds ~950 stems.
2. **Reject ugly fusions.** Discard the candidate and retry (up to 8 times) if it exceeds 12 characters, repeats a letter three times in a row, or forms a bad seam at the junction — a doubled-identical-vowel sound (`aa ee ii oo uu yy iy yi`) in the `±2`-character window around the join.
3. **One syllable rotation.** Find every spot where a rotation rule matches and apply exactly **one**, chosen at random. Rotations are syllable-preserving CV swaps (`pa→po`, `ti→ty`, `ki→ky` …) plus a few unambiguous letter swaps (`k↔q`, `c↔k`, `ph↔f`, `x↔ks`). There is no class-wide single-letter rotation.
4. **Capitalize the first letter.**

Seeded by the current timestamp (`Date.now()` / `time_ns()` / system clock) by default; pass an integer seed for reproducible output. ASCII only, no network.

The four implementations are equivalent **in spirit, not bit-identical** — each language seeds and draws from its own RNG, so the same seed yields different names across languages. `scripts/generate_data.py` is the single source of truth for the vocabulary; it regenerates every per-language wordlist. The TypeScript implementation is the reference for the demo page.

## Build & publish

```bash
./build.sh            # build TS, Python wheel, Rust crate, C++ binary
./publish.sh          # publish TS → npm, Python → PyPI, Rust → crates.io
./publish.sh --dry-run
```

See each subfolder's README for language-specific usage.

## License

MIT. © 2026 Adam Twardoch.
