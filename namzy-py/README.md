# namzy

Generate fun, human-friendly fused project names from a bundled local wordlist.

## Install

```bash
pip install namzy
# or run without installing:
uvx namzy
```

## CLI usage

```bash
namzy

# Multiple names
namzy --count 5

# Reproducible output
namzy --seed 42 --count 3
```

## Library usage

```python
from namzy import generate

name = generate()

# Reproducible
name = generate(seed=42)
```

## Wordlist

Namzy uses the shared bundled wordlists of 500 geographic names and 500 common words. Each pair may be joined in either order, for 500,000 raw ordered pairings before seam cleanup and replacement collisions. No network required.

## Mangling

Names pass through seam cleanup, then activate a seed-derived subset of 1 to 10 replacement rules from `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u · b→p · p→b`.

## License

MIT
