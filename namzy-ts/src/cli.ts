#!/usr/bin/env node
// this_file: src/cli.ts

import { generate } from "./index.js";
import type { NamzyOptions } from "./index.js";

const HELP = `
namzy — generate fun fused project names

Usage:
  namzy [options]

Options:
  --online        Fetch words from a public API (falls back to offline)
  --count <N>     Number of names to generate (default: 1)
  --help          Show this help

Examples:
  namzy
  namzy --count 5
  namzy --online --count 3
`.trimStart();

function parseArgs(argv: string[]): { opts: NamzyOptions; count: number } {
  const args = argv.slice(2);
  const opts: NamzyOptions = {};
  let count = 1;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case "--help":
      case "-h":
        process.stdout.write(HELP);
        process.exit(0);
        break;
      case "--online":
        opts.online = true;
        break;
      case "--count": {
        const n = parseInt(args[++i], 10);
        if (isNaN(n) || n < 1) {
          process.stderr.write(`--count must be a positive integer\n`);
          process.exit(1);
        }
        count = n;
        break;
      }
      default:
        process.stderr.write(`Unknown flag: ${arg}\nRun namzy --help for usage.\n`);
        process.exit(1);
    }
  }
  return { opts, count };
}

async function main(): Promise<void> {
  const { opts, count } = parseArgs(process.argv);
  const base = Date.now();
  for (let i = 0; i < count; i++) {
    const name = await generate({ ...opts, seed: base + i * 1337 });
    process.stdout.write(name + "\n");
  }
}

main().catch((err) => {
  process.stderr.write(`Error: ${err instanceof Error ? err.message : String(err)}\n`);
  process.exit(1);
});
