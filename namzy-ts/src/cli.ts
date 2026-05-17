#!/usr/bin/env node
// this_file: src/cli.ts

import { generate } from "./index.js";

const HELP = `
namzy — generate compact, memorable, unique names

Usage:
  namzy [options]

Options:
  --count <N>     Number of names to generate (default: 1)
  --seed <N>      Integer seed (default: current timestamp)
  --help          Show this help
`.trimStart();

function parseArgs(argv: string[]): { count: number; seed?: number } {
  const args = argv.slice(2);
  let count = 1;
  let seed: number | undefined;
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case "--help":
      case "-h":
        process.stdout.write(HELP);
        process.exit(0);
        break;
      case "--count": {
        const n = parseInt(args[++i], 10);
        if (Number.isNaN(n) || n < 1) {
          process.stderr.write("--count must be a positive integer\n");
          process.exit(1);
        }
        count = n;
        break;
      }
      case "--seed": {
        const n = parseInt(args[++i], 10);
        if (Number.isNaN(n)) {
          process.stderr.write("--seed must be an integer\n");
          process.exit(1);
        }
        seed = n;
        break;
      }
      default:
        process.stderr.write(`Unknown flag: ${arg}\nRun namzy --help for usage.\n`);
        process.exit(1);
    }
  }
  return { count, seed };
}

function main(): void {
  const { count, seed } = parseArgs(process.argv);
  const base = seed ?? Date.now();
  for (let i = 0; i < count; i++) {
    process.stdout.write(`${generate({ seed: base + i * 2654435761 })}\n`);
  }
}

main();
