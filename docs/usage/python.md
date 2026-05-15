---
title: Python
permalink: /usage/python/
nav_order: 3
---

# Python

The Python package is `namzy` on PyPI. It requires Python 3.10 or newer.

## Install

```bash
python -m pip install namzy
```

## Generate a name

```python
from namzy import generate

name = generate()
print(name)
```

`generate()` returns a `str`.

## Options

Use `seed` for repeatable generation:

```python
print(generate(seed=42))
```

Namzy picks one geographic word and one common word from the shared bundled lists, then randomly joins either geographic+common or common+geographic. That gives 180,000 raw ordered source pairings before cleanup and mangling.

Function signature:

```python
generate(seed: int | None = None) -> str
```

## CLI

After installation, run:

```bash
namzy --count 5
```

With a deterministic seed:

```bash
namzy --count 5 --seed 42
```

You can also run the package without installing it into the current environment:

```bash
uvx namzy --count 5
```

CLI flags:

| Flag | Description |
| --- | --- |
| `--count N` | Print `N` names. Defaults to `1`. |
| `--seed INT` | Seed the generator. For multiple names, each item increments the seed. |
