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

Namzy uses the shared bundled wordlists of 300 geographic names and 300 common words. Each pair may be joined in either order, for 180,000 raw ordered pairings before seam cleanup and mangling. No network required.

## Mangling

Names pass through seam cleanup and the consonant rotation `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u`.

## License

MIT
