---
title: TypeScript / JavaScript
permalink: /usage/typescript-javascript/
nav_order: 1
---

# TypeScript / JavaScript

The npm package is `@twardoch/namzy`. It is an ES module package for Node.js 18 and newer.

## Install

```bash
npm install @twardoch/namzy
```

## Generate a name

```js
import { generate } from "@twardoch/namzy";

const name = await generate();
console.log(name);
```

`generate()` returns a `Promise<string>`.

## Options

Use `seed` for repeatable offline generation:

```js
const name = await generate({ seed: 42 });
```

Use `online: true` to request source words from the public random-word API. If the request fails, Namzy falls back to bundled wordlists.

```js
const name = await generate({ online: true });
```

Available options:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `online` | `boolean` | `false` | Fetch source words online, then fall back to bundled wordlists if needed. |
| `seed` | `number` | current timestamp | Seed the offline pseudo-random generator. |

The package also exports `joinClean`, `mangle`, `mulberry32`, `GEO`, and `COMMON` for lower-level use.

## CLI

Run without installing globally:

```bash
npx @twardoch/namzy --count 5
```

Use online source words:

```bash
npx @twardoch/namzy --online --count 5
```

CLI flags:

| Flag | Description |
| --- | --- |
| `--count <N>` | Print `N` names. Defaults to `1`. |
| `--online` | Try online source words before falling back to bundled wordlists. |
| `--help`, `-h` | Show help. |
