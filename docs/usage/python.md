---
title: Python
permalink: /usage/python/
description: Install and use namzy from PyPI.
parent: Usage
nav_order: 2
---

The Python package is [`namzy`](https://pypi.org/project/namzy/) on PyPI and requires Python 3.10+.

## Install

```bash
python -m pip install namzy
```

## Generate one name

```python
from namzy import generate

name = generate()
print(name)
```

## Use a deterministic seed

```python
from namzy import generate

print(generate(seed=42))
```

## Try online words

```python
from namzy import generate

print(generate(online=True))
```

Online mode asks the public random-word API for source words and falls back to bundled words on network errors.

## CLI

```bash
namzy --count 5
namzy --seed 42 --count 3
namzy --online --count 3
```

With [`uv`](https://docs.astral.sh/uv/), you can also run it without a separate install:

```bash
uvx namzy --count 5
```

CLI options:

- `--count N`: print `N` names, default `1`.
- `--seed INT`: seed the offline generator; repeated names increment from that seed.
- `--online`: request random source words before falling back to bundled words.
