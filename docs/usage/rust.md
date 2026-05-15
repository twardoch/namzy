---
title: Rust
permalink: /usage/rust/
parent: Usage
nav_order: 3
---

# Rust

The Rust crate is `namzy` on crates.io.

## Install

Add the crate to a project:

```bash
cargo add namzy
```

Install the command-line tool:

```bash
cargo install namzy
```

## Generate a name

```rust
use namzy::{generate, Options};

fn main() {
    let name = generate(&Options {
        seed: None,
    });

    println!("{name}");
}
```

`generate()` returns a `String`.

## Options

Use a seed for repeatable generation:

```rust
let name = generate(&Options {
    seed: Some(42),
});
```

Namzy picks one geographic word and one common word from the shared bundled lists, then randomly joins either geographic+common or common+geographic. That gives 180,000 raw ordered source pairings before cleanup and mangling.

The crate also exposes `join_clean()` and `Mulberry32` for lower-level use.

## CLI

```bash
namzy --count 5
```

With a deterministic seed:

```bash
namzy --count 5 --seed 42
```

CLI flags:

| Flag | Description |
| --- | --- |
| `--count <COUNT>` | Print the requested number of names. Defaults to `1`. |
| `--seed <SEED>` | Seed the generator. For multiple names, each item increments the seed. |
