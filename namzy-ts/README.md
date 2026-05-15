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

Namzy uses the shared bundled wordlists of 300 geographic words and 300 common words. Each pair may be joined in either order, for 180,000 raw ordered pairings before seam cleanup and mangling.

## How it works

Picks one geographic name and one evocative common word, joins them in either order, cleans awkward seams, and applies the consonant rotation `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u`. Results are deterministic for a given seed.

## License

MIT
