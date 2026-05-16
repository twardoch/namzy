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
- Namzy uses the same bundled 500 geographic words and 500 common words across every implementation;
- each source pair can be joined as geographic+common or common+geographic, for 500,000 raw ordered pairings;
- a seed can make library calls repeatable where the implementation exposes one.

Choose a language:

- [JavaScript]({{ '/usage/javascript/' | relative_url }})
- [Python]({{ '/usage/python/' | relative_url }})
- [Rust]({{ '/usage/rust/' | relative_url }})
- [C++]({{ '/usage/cpp/' | relative_url }})
