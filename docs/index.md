---
layout: page
title: namzy
description: Fun, fused, mangled project names.
permalink: /
nav_order: 1
has_toc: false
---

<link rel="stylesheet" href="{{ '/assets/css/namzy.css' | relative_url }}">

<section class="namzy-hero">
  <p class="namzy-hero__lede">Fun, fused, mangled project names. Namzy picks two words, splices them at a clean junction, rotates selected consonants, and returns one pronounceable token.</p>
</section>

<section class="namzy-demo" aria-labelledby="demo-title">
  <h2 id="demo-title">Try the generator</h2>
  <fieldset>
    <legend>Options</legend>
    <div class="namzy-demo__controls">
      <label>
        Count
        <input type="number" id="count" min="1" max="50" value="6">
      </label>
      <label class="namzy-demo__check">
        <input type="checkbox" id="online">
        Online mode
      </label>
      <button id="go" type="button">Generate</button>
    </div>
  </fieldset>
  <ul class="namzy-demo__names" id="out" aria-live="polite"></ul>
  <p class="namzy-note">Online mode asks a public random-word API for source words and falls back to bundled wordlists if the request fails.</p>
</section>

<p class="namzy-note">Mangling rotates <code>c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u</code>. Junction cleanup drops a duplicate letter or a vowel-on-vowel clash at the seam.</p>

## Use namzy anywhere

<div class="namzy-card-grid">
  <a class="namzy-card" href="{{ '/usage/typescript-javascript/' | relative_url }}">
    <h3>TypeScript / JavaScript</h3>
    <p>Install <code>@twardoch/namzy</code>, import <code>generate</code>, or run the <code>namzy</code> CLI with Node 18+.</p>
  </a>
  <a class="namzy-card" href="{{ '/usage/python/' | relative_url }}">
    <h3>Python</h3>
    <p>Install <code>namzy</code> from PyPI, call <code>generate()</code>, or use the console command.</p>
  </a>
  <a class="namzy-card" href="{{ '/usage/rust/' | relative_url }}">
    <h3>Rust</h3>
    <p>Add the <code>namzy</code> crate, call <code>generate(&Options)</code>, or install the binary.</p>
  </a>
  <a class="namzy-card" href="{{ '/usage/cpp-qt5/' | relative_url }}">
    <h3>C++ / Qt 5</h3>
    <p>Build the Qt5-compatible C++ implementation and embed <code>Namzy</code> in Qt apps.</p>
  </a>
</div>

<script src="{{ '/namzy.js' | relative_url }}"></script>
<script>
  const $ = (id) => document.getElementById(id);
  const out = $("out");
  const btn = $("go");

  async function run() {
    out.innerHTML = "";
    const count = Math.max(1, Math.min(50, parseInt($("count").value, 10) || 1));
    const online = $("online").checked;
    const base = Date.now();
    btn.disabled = true;
    try {
      for (let i = 0; i < count; i++) {
        const name = await namzy.generate({ online, seed: base + i * 1337 });
        const li = document.createElement("li");
        li.textContent = name;
        out.appendChild(li);
      }
    } catch (e) {
      const li = document.createElement("li");
      li.textContent = "Error: " + e.message;
      out.appendChild(li);
    } finally {
      btn.disabled = false;
    }
  }

  btn.addEventListener("click", run);
  run();
</script>
