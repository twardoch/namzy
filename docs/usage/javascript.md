---
title: JavaScript
permalink: /usage/javascript/
parent: Usage
nav_order: 1
---

# JavaScript

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

Use `seed` for repeatable generation:

```js
const name = await generate({ seed: 42 });
```

Namzy picks one geographic word and one common word from the shared bundled lists, then randomly joins either geographic+common or common+geographic. That gives 500,000 raw ordered source pairings before seam cleanup and replacement collisions.

Available options:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `seed` | `number` | current timestamp | Seed the offline pseudo-random generator. |

The package also exports `joinClean`, `mangle`, `mulberry32`, `GEO`, and `COMMON` for lower-level use.

## CLI

Run without installing globally:

```bash
npx @twardoch/namzy --count 5
```

CLI flags:

| Flag | Description |
| --- | --- |
| `--count <N>` | Print `N` names. Defaults to `1`. |
| `--help`, `-h` | Show help. |
