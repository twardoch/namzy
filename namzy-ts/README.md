# namzy

Generates fun, human-friendly fused project names from a bundled local wordlist.

## Install

```sh
npm install @twardoch/namzy
# or run without installing:
npx @twardoch/namzy
```

## CLI

```sh
npx @twardoch/namzy

# Generate 5 names
npx @twardoch/namzy --count 5

# Help
npx @twardoch/namzy --help
```

## Library

```ts
import { generate } from "@twardoch/namzy";

const name = await generate();

// Seeded for reproducibility
const seeded = await generate({ seed: 42 });

console.log(name, seeded);
```

## Wordlist

Namzy uses the shared bundled wordlists of 500 geographic words and 500 common words. Each pair may be joined in either order, for 500,000 raw ordered pairings before seam cleanup and replacement collisions.

## How it works

Picks one geographic name and one evocative common word, joins them in either order, cleans awkward seams, then activates a seed-derived subset of 1 to 10 replacement rules from `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u · b→p · p→b`. Results are deterministic for a given seed.

## License

MIT
