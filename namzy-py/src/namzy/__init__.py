# this_file: src/namzy/__init__.py
"""namzy — fun human-friendly project name generator."""

from __future__ import annotations

import random
import time

from ._mangle import join_clean, mangle
from ._wordlist import COMMON, GEO

__version__ = "0.2.0"

__all__ = ["generate"]

_ONLINE_URL_TWO = "https://random-word-api.herokuapp.com/word?number=2&length=6"


def _fetch_online() -> list[str] | None:
    """Fetch two words from a public API. Returns None on any error."""
    try:
        import json
        import urllib.request

        with urllib.request.urlopen(_ONLINE_URL_TWO, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            if isinstance(data, list):
                words = [w for w in data if w.isalpha()]
                if len(words) >= 2:
                    return words[:2]
    except Exception:
        pass
    return None


def _pick_words(rng: random.Random, online: bool) -> tuple[str, str]:
    """Return two raw lowercase words."""
    if online:
        fetched = _fetch_online()
        if fetched:
            return fetched[0].lower(), fetched[1].lower()
    return rng.choice(GEO).lower(), rng.choice(COMMON).lower()


def generate(online: bool = False, seed: int | None = None) -> str:
    """Generate a fun project name.

    Picks two words, fuses them with junction cleanup, applies consonant
    rotation, and capitalizes the first letter.
    """
    if seed is None:
        seed = time.time_ns()
    rng = random.Random(seed)

    a, b = _pick_words(rng, online)
    fused = join_clean(a, b)
    rotated = mangle(fused)
    return rotated[:1].upper() + rotated[1:]
