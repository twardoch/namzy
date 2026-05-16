# namzy-rs

Generates fun, human-friendly fused project names from a bundled local wordlist.

## Install

```sh
cargo install --path .
```

## CLI Usage

```sh
namzy

# Generate 5 names
namzy --count 5

# Fixed seed for reproducibility
namzy --seed 12345 --count 3
```

## Library Usage

```rust
use namzy::{generate, Options};

let name = generate(&Options {
    seed: Some(42),
});
println!("{}", name);
```

## Wordlist

Namzy uses the shared bundled wordlists of 500 geographic names and 500 common words. Each pair may be joined in either order, for 500,000 raw ordered pairings before seam cleanup and replacement collisions.

Words pass through seam cleanup, then activate a seed-derived subset of 1 to 10 replacement rules from `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u · b→p · p→b`.
