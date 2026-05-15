---
title: Python
permalink: /usage/python/
nav_order: 2
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

Use `seed` for repeatable offline generation:

```python
print(generate(seed=42))
```

Use `online=True` to request source words from the public random-word API. If the request fails, Namzy falls back to the shared 300 x 300 bundled wordlists.

```python
print(generate(online=True))
```

Function signature:

```python
generate(online: bool = False, seed: int | None = None) -> str
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

With online source words:

```bash
namzy --online --count 5
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
| `--online` | Try online source words before falling back to bundled wordlists. |
