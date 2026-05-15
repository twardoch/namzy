---
title: Rust
permalink: /usage/rust/
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
        online: false,
        seed: None,
    });

    println!("{name}");
}
```

`generate()` returns a `String`.

## Options

Use a seed for repeatable offline generation:

```rust
let name = generate(&Options {
    online: false,
    seed: Some(42),
});
```

Use online source words:

```rust
let name = generate(&Options {
    online: true,
    seed: None,
});
```

If the online request fails, Namzy falls back to bundled wordlists.

The crate also exposes `join_clean()` and `Mulberry32` for lower-level use.

## CLI

```bash
namzy --count 5
```

With a deterministic seed:

```bash
namzy --count 5 --seed 42
```

With online source words:

```bash
namzy --online --count 5
```

CLI flags:

| Flag | Description |
| --- | --- |
| `--count <COUNT>` | Print the requested number of names. Defaults to `1`. |
| `--seed <SEED>` | Seed the generator. For multiple names, each item increments the seed. |
| `--online` | Try online source words before falling back to bundled wordlists. |
