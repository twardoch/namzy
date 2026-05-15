"use strict";
var namzy = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // src/web.ts
  var web_exports = {};
  __export(web_exports, {
    COMMON: () => COMMON,
    GEO: () => GEO,
    generate: () => generate,
    joinClean: () => joinClean,
    mangle: () => mangle,
    mulberry32: () => mulberry32
  });

  // src/wordlist.ts
  var GEO = [
    "tokyo",
    "paris",
    "oslo",
    "berlin",
    "lagos",
    "lima",
    "boston",
    "vienna",
    "cairo",
    "kyoto",
    "dubai",
    "seoul",
    "milan",
    "tunis",
    "perth",
    "genoa",
    "porto",
    "bruges",
    "ghent",
    "brest",
    "minsk",
    "sofia",
    "riga",
    "lyon",
    "basel",
    "natal",
    "recife",
    "darwin",
    "hobart",
    "odessa",
    "varna",
    "Split",
    "kotor",
    "tiran",
    "skopje",
    "bitola",
    "plovdiv",
    "gabrovo",
    "varna",
    "ruse"
  ];
  var COMMON = [
    "river",
    "stone",
    "ember",
    "frost",
    "harbor",
    "willow",
    "copper",
    "marble",
    "anchor",
    "lantern",
    "cedar",
    "falcon",
    "coral",
    "dagger",
    "flint",
    "grove",
    "haven",
    "iron",
    "jasper",
    "kelp",
    "larch",
    "mast",
    "nettle",
    "oak",
    "pine",
    "quill",
    "reed",
    "sage",
    "thorn",
    "umber",
    "vale",
    "wren",
    "yarrow",
    "zenith",
    "amber",
    "birch",
    "cliff",
    "drift",
    "forge",
    "glade"
  ];

  // src/mangle.ts
  function mulberry32(seed) {
    let s = seed >>> 0;
    return () => {
      s += 1831565813;
      let t = Math.imul(s ^ s >>> 15, 1 | s);
      t ^= t + Math.imul(t ^ t >>> 7, 61 | t);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  var ROTATION = {
    c: "q",
    f: "v",
    k: "c",
    q: "k",
    s: "z",
    z: "s",
    v: "f",
    w: "u"
  };
  function mangle(s) {
    let out = "";
    for (const ch of s) {
      const lower = ch.toLowerCase();
      const repl = ROTATION[lower];
      if (repl === void 0) {
        out += ch;
      } else {
        out += ch === lower ? repl : repl.toUpperCase();
      }
    }
    return out;
  }
  var VOWELS = /* @__PURE__ */ new Set(["a", "e", "i", "o", "u", "y"]);
  function joinClean(a, b) {
    let head = a;
    let tail = b;
    for (let i = 0; i < 2 && head.length > 0 && tail.length > 0; i++) {
      const last = head[head.length - 1].toLowerCase();
      const first = tail[0].toLowerCase();
      if (last === first) {
        tail = tail.slice(1);
      } else if (VOWELS.has(last) && VOWELS.has(first)) {
        tail = tail.slice(1);
      } else {
        break;
      }
    }
    return head + tail;
  }

  // src/index.ts
  function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }
  function pick(arr, rng) {
    return arr[Math.floor(rng() * arr.length)];
  }
  async function fetchOnlineWords() {
    const url = `https://random-word-api.herokuapp.com/word?number=2&length=6`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    if (!Array.isArray(data) || data.length < 2) throw new Error("Bad response");
    return data.slice(0, 2).map((w) => w.toLowerCase().replace(/[^a-z]/g, ""));
  }
  async function generate(opts) {
    const online = opts?.online ?? false;
    const seed = opts?.seed ?? Date.now();
    const rng = mulberry32(seed);
    let w1;
    let w2;
    if (online) {
      try {
        const words = await fetchOnlineWords();
        [w1, w2] = words;
      } catch {
        w1 = pick(GEO, rng).toLowerCase();
        w2 = pick(COMMON, rng).toLowerCase();
      }
    } else {
      w1 = pick(GEO, rng).toLowerCase();
      w2 = pick(COMMON, rng).toLowerCase();
    }
    const fused = joinClean(w1, w2);
    return capitalize(mangle(fused));
  }
  return __toCommonJS(web_exports);
})();
