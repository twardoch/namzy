---
title: Usage
permalink: /usage/
description: Install and use namzy across TypeScript, JavaScript, Python, Rust, and C++ with Qt 5.
nav_order: 2
has_children: true
has_toc: true
---

Namzy implementations share the same contract: return one fused token from two source words. The exact wordlists and random streams are implementation-specific, so outputs are equivalent in spirit rather than bit-identical across languages.

## Shared options

- `online`: fetch two random words from the public random-word API, then fall back to bundled words if the request fails.
- `seed`: make offline generation repeatable where the language binding exposes it.
- `count`: CLI-only repeat count for printing several names.

## Language guides

- [TypeScript / JavaScript]({{ '/usage/typescript-javascript/' | relative_url }})
- [Python]({{ '/usage/python/' | relative_url }})
- [Rust]({{ '/usage/rust/' | relative_url }})
- [C++ / Qt 5]({{ '/usage/cpp-qt5/' | relative_url }})

## Naming pipeline

1. Pick one geo-ish word and one common word.
2. Join them with seam cleanup: duplicate letters and vowel-on-vowel clashes are dropped up to twice.
3. Rotate selected consonants: `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u`.
4. Capitalize the fused token.
