---
title: Usage
permalink: /usage/
nav_order: 2
has_children: true
has_toc: false
---

# Usage

Namzy has sibling implementations for TypeScript/JavaScript, Python, Rust, and C++/Qt 5.

Each implementation follows the same basic contract:

- output is one fused name token;
- offline mode uses the same bundled 300 geographic words and 300 common words across every implementation, for 90,000 raw pairings;
- online mode asks a public random-word API for source words and falls back to bundled wordlists if needed;
- a seed can make library calls repeatable where the implementation exposes one.

Choose a language:

- [TypeScript / JavaScript]({{ '/usage/typescript-javascript/' | relative_url }})
- [Python]({{ '/usage/python/' | relative_url }})
- [Rust]({{ '/usage/rust/' | relative_url }})
- [C++ / Qt 5]({{ '/usage/cpp/' | relative_url }})
