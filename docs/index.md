---
layout: page
title: namzy
description: Fun, fused, mangled project names.
permalink: /
has_toc: false
---

<link rel="stylesheet" href="{{ '/assets/css/namzy.css' | relative_url }}">

<section class="namzy-hero">
  <p class="namzy-hero__lede">Fun, fused, mangled project names. Namzy picks two words, splices them at a clean junction, rotates selected consonants, and returns one pronounceable token.</p>
</section>

<section class="namzy-demo" aria-labelledby="demo-title">
  <div class="namzy-demo__head">
    <div>
      <p class="namzy-demo__eyebrow">Generator</p>
      <h2 id="demo-title">Make a short list</h2>
    </div>
    <button id="go" type="button">Generate</button>
  </div>
  <fieldset>
    <div class="namzy-demo__controls">
      <label class="namzy-demo__field">
        <span>Count</span>
        <input type="number" id="count" min="1" max="50" value="6">
      </label>
      <label class="namzy-demo__check">
        <input type="checkbox" id="online">
        <span>Online words</span>
      </label>
    </div>
  </fieldset>
  <label class="namzy-demo__output">
    <span>Names</span>
    <textarea id="out" rows="8" readonly spellcheck="false" aria-live="polite"></textarea>
  </label>
  <p class="namzy-note">Online mode asks a public random-word API for source words and falls back to bundled wordlists if the request fails.</p>
</section>

<p class="namzy-note">Mangling rotates <code>c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u</code>. Junction cleanup drops a duplicate letter or a vowel-on-vowel clash at the seam.</p>

## Install

```bash
npm install @twardoch/namzy
python -m pip install namzy
cargo add namzy
```

For C++ / Qt 5, build the source package:

```bash
cmake -S namzy-cpp -B namzy-cpp/build
cmake --build namzy-cpp/build
```

## Use

### TypeScript / JavaScript

```js
import { generate } from "@twardoch/namzy";

console.log(await generate({ seed: 42 }));
```

CLI:

```bash
npx @twardoch/namzy --count 5
```

### Python

```python
from namzy import generate

print(generate(seed=42))
```

CLI:

```bash
namzy --count 5 --seed 42
```

### Rust

```rust
use namzy::{generate, Options};

fn main() {
    let name = generate(&Options { online: false, seed: Some(42) });
    println!("{name}");
}
```

CLI:

```bash
cargo install namzy
namzy --count 5 --seed 42
```

### C++ / Qt 5

```cpp
#include "namzy.h"

Namzy generator(42);
QString offline = generator.generateOffline();
QString online = generator.generateOnline();
```

Link against Qt 5 Core and Network.

<script src="{{ '/namzy.js' | relative_url }}"></script>
<script>
  const $ = (id) => document.getElementById(id);
  const out = $("out");
  const btn = $("go");

  async function run() {
    out.value = "";
    const count = Math.max(1, Math.min(50, parseInt($("count").value, 10) || 1));
    const online = $("online").checked;
    const base = Date.now();
    btn.disabled = true;
    try {
      const names = [];
      for (let i = 0; i < count; i++) {
        const name = await namzy.generate({ online, seed: base + i * 1337 });
        names.push(name);
      }
      out.value = names.join("\n");
    } catch (e) {
      out.value = "Error: " + e.message;
    } finally {
      btn.disabled = false;
    }
  }

  btn.addEventListener("click", run);
  run();
</script>
