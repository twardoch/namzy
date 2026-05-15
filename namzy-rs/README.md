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

Namzy uses the shared bundled wordlists of 300 geographic names and 300 common words. Each pair may be joined in either order, for 180,000 raw ordered pairings before seam cleanup and mangling.

Words pass through seam cleanup and the consonant rotation `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u`.
