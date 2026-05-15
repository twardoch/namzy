# namzy

Generate fun, human-friendly project names — seeded by time, mangled for personality.

## Install

```bash
pip install namzy
# or run without installing:
uvx namzy
```

## CLI usage

```bash
# One name, single word (default)
namzy

# Multiple names
namzy --count 5

# Output shapes
namzy --shape single    # e.g. Tokyuriver
namzy --shape joined    # e.g. TokyuRiver
namzy --shape spaced    # e.g. Tokyu River

# Reproducible output
namzy --seed 42 --count 3

# Fetch words from a public API (falls back to offline on error)
namzy --online --count 3
```

## Library usage

```python
from namzy import generate

# Single word (default)
name = generate()

# Joined PascalCase
name = generate(shape="joined")

# Spaced words
name = generate(shape="spaced")

# Reproducible
name = generate(seed=42)

# Online mode
name = generate(online=True)
```

## Modes

- **Offline** (default): Uses a bundled wordlist of ~40 geographic names and ~40 evocative English nouns. No network required.
- **Online**: Fetches two words from `random-word-api.herokuapp.com`. Falls back silently to offline on any error.

## Mangling

Names pass through a phonetic mangling pass: `tion→shun`, `ight→ite`, `oo→u`, `ck→kk`, `ph→f`, `ks→x`, trailing `s→z`. One or two substitutions apply randomly per word.

## License

MIT
