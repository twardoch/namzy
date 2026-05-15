---
title: Rust
permalink: /usage/rust/
description: Install and use the namzy crate from crates.io.
parent: Usage
nav_order: 3
---

The Rust crate is [`namzy`](https://crates.io/crates/namzy) on crates.io. It provides both a library and a CLI binary.

## Add the library

```bash
cargo add namzy
```

## Generate one name

```rust
use namzy::{generate, Options};

fn main() {
    let name = generate(&Options {
        online: false,
        seed: None,
    });

    println!("{name}");
}
```

## Use a deterministic seed

```rust
use namzy::{generate, Options};

fn main() {
    let name = generate(&Options {
        online: false,
        seed: Some(42),
    });

    println!("{name}");
}
```

## Try online words

```rust
use namzy::{generate, Options};

fn main() {
    let name = generate(&Options {
        online: true,
        seed: None,
    });

    println!("{name}");
}
```

Online mode uses a blocking HTTP request through the crate implementation and falls back to bundled words when the request fails.

## CLI

```bash
cargo install namzy
namzy --count 5
namzy --seed 42 --count 3
namzy --online --count 3
```

CLI options:

- `--count <N>`: print `N` names, default `1`.
- `--seed <SEED>`: seed the offline generator; repeated names increment from that seed.
- `--online`: request random source words before falling back to bundled words.
