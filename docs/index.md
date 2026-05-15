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
  <h2 id="demo-title">Make a short list</h2>
  <fieldset>
    <div class="namzy-demo__controls">
      <label class="namzy-demo__field">
        <span>Count</span>
        <input type="number" id="count" min="1" max="50" value="6">
      </label>
    </div>
  </fieldset>
  <button id="go" type="button">Generate</button>
  <label class="namzy-demo__output">
    <span>Names</span>
    <textarea id="out" rows="8" readonly spellcheck="false" aria-live="polite"></textarea>
  </label>
</section>

<p class="namzy-note">Mangling rotates <code>c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u</code>. Junction cleanup drops a duplicate letter or a vowel-on-vowel clash at the seam.</p>

## Usage

Choose the page for the language you use:

- [JavaScript]({{ '/usage/javascript/' | relative_url }})
- [Python]({{ '/usage/python/' | relative_url }})
- [Rust]({{ '/usage/rust/' | relative_url }})
- [C++]({{ '/usage/cpp/' | relative_url }})

All implementations return one fused name token. Namzy uses the same bundled 300 geographic words and 300 common words across every implementation, and can join them in either order. That makes 180,000 raw ordered source-word pairings before seam cleanup and consonant rotation.

<script src="{{ '/namzy.js' | relative_url }}"></script>
<script>
  const $ = (id) => document.getElementById(id);
  const out = $("out");
  const btn = $("go");

  async function run() {
    out.value = "";
    const count = Math.max(1, Math.min(50, parseInt($("count").value, 10) || 1));
    const base = Date.now();
    btn.disabled = true;
    try {
      const names = [];
      for (let i = 0; i < count; i++) {
        const name = await namzy.generate({ seed: base + i * 1337 });
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
