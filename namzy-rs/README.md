# namzy-rs

Generates fun, human-friendly project names. Seeded by timestamp for reproducibility.

## Install

```sh
cargo install --path .
```

## CLI Usage

```sh
# Single word (default)
namzy
# → Oslu

# Two-word PascalCase
namzy --shape joined
# → PragueEmber

# Two words with space
namzy --shape spaced
# → Prague Ember

# Generate 5 names
namzy --shape joined --count 5

# Fixed seed for reproducibility
namzy --seed 12345 --shape spaced

# Online mode (fetches from random-word API, falls back offline)
namzy --online --shape joined
```

## Library Usage

```rust
use namzy::{generate, Options, Shape};

let name = generate(&Options {
    shape: Shape::Joined,
    online: false,
    seed: Some(42),
});
println!("{}", name); // e.g. "TokyoRiver"
```

## Modes

- **Offline** (default): uses bundled wordlist of ~40 geographic names + ~40 common English words.
- **Online**: fetches from `random-word-api.herokuapp.com`; silently falls back to offline on any error.

## Output Shapes

| Shape    | Example         |
|----------|-----------------|
| `single` | `Oslu`          |
| `joined` | `OsluEmber`     |
| `spaced` | `Oslu Ember`    |

Words pass through a small phonetic mangling pass (e.g. `oo→u`, `tion→shun`, trailing `s→z`).
