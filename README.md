# namzy

`namzy` generates fun, human-friendly project names for software or typefaces. It picks two words from a built-in (or online) vocabulary, fuses them at a clean junction so the result reads as a single word, and runs the seam through a small consonant rotation. The output looks invented but stays pronounceable — e.g. `Pariznimble`, `Luzacanlet`, `Boyzcraeft`.

A live demo lives in [`docs/index.html`](./docs/index.html) (also browsable via GitHub Pages once enabled).

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

All four implementations behave the same way:

1. **Two words → one fused name.** Always. There is no "single word" or "Two Word" mode — the result is always one fused token that *looks* like one word but is two.
2. **Junction cleanup at the seam.** When the end of word 1 meets the start of word 2:
   - if the letters are the same, drop one;
   - if both letters are vowels (`a e i o u y`), drop one.
   Applied up to twice. This removes awkward joins like `nordaarctic` → `nordarctic`.
3. **Consonant rotation pass.** A small, case-preserving per-letter map applied to the fused string:
   `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u`
4. **Timestamp seed.** Seeded by `Date.now()` / `time_ns()` / system clock by default; a caller-supplied seed gives reproducible output.
5. **Vocabulary.** Basic `A-Za-z` only, drawn from geographic names and common Latin-alphabet words. No diacritics.
6. **Two modes.**
   - *Bundled* — shared 300 geographic words x 300 common words (90,000 raw pairings) shipped with every implementation; no network.
   - *Online* — fetches from a public no-auth API; falls back to bundled on failure.

The four implementations are equivalent in spirit, not bit-identical. The TS implementation is the reference for the demo page.

## Build & publish

```bash
./build.sh            # build TS, Python wheel, Rust crate, C++ binary
./publish.sh          # publish TS → npm, Python → PyPI, Rust → crates.io
./publish.sh --dry-run
```

See each subfolder's README for language-specific usage.

## License

MIT. © 2026 Adam Twardoch.
