---
title: TypeScript / JavaScript
permalink: /usage/typescript-javascript/
description: Install and use @twardoch/namzy from npm.
parent: Usage
nav_order: 1
---

The npm package is [`@twardoch/namzy`](https://www.npmjs.com/package/@twardoch/namzy). It targets Node.js 18+ and ships ESM plus TypeScript declarations.

## Install

```bash
npm install @twardoch/namzy
```

## Generate one name

```ts
import { generate } from "@twardoch/namzy";

const name = await generate();
console.log(name);
```

## Use a deterministic seed

```ts
import { generate } from "@twardoch/namzy";

console.log(await generate({ seed: 42 }));
```

## Try online words

```ts
import { generate } from "@twardoch/namzy";

const name = await generate({ online: true });
```

Online mode uses a public random-word API and falls back to bundled words on request failure.

## CLI

```bash
npx @twardoch/namzy --count 5
npx @twardoch/namzy --online --count 3
```

CLI options:

- `--count <N>`: print `N` names, default `1`.
- `--online`: request random source words before falling back to bundled words.
- `--help`: show command help.

## Utility exports

The package also exports `joinClean`, `mangle`, `mulberry32`, `GEO`, and `COMMON` for advanced use.
