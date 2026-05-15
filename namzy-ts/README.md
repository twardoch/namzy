# namzy

Generates fun, human-friendly project names. Seeded by timestamp so you get
fresh names every run — but pass `--seed` for reproducibility.

## Install

```sh
npm install namzy
# or run without installing:
npx namzy
```

## CLI

```sh
# One word (default)
namzy

# PascalCase two-word name
namzy --shape joined

# Space-separated two words
namzy --shape spaced

# Generate 5 names
namzy --count 5 --shape joined

# Fetch words from the web (falls back to offline on failure)
namzy --online --shape spaced

# Help
namzy --help
```

## Library

```ts
import { generate } from "namzy";

// Single word (default)
const name = await generate();

// Joined PascalCase
const joined = await generate({ shape: "joined" });

// Spaced, seeded for reproducibility
const seeded = await generate({ shape: "spaced", seed: 42 });

// Online mode (falls back to offline)
const online = await generate({ online: true, shape: "joined" });

console.log(name, joined, seeded, online);
```

## Modes

| Mode | Description |
|------|-------------|
| `--offline` | Uses bundled wordlist (default, always works) |
| `--online` | Fetches from `random-word-api.herokuapp.com`, falls back offline |

## How it works

Picks words from geographic names (Tokyo, Oslo, Cairo…) and evocative English
words (ember, flint, willow…), then applies a small phonetic mangling pass
(e.g. `s→z`, `ph→f`, `oo→u`) for a playful feel. Results are deterministic
for a given seed.

## License

MIT
