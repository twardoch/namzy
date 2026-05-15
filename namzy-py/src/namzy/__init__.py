# this_file: src/namzy/__init__.py
"""namzy — fun human-friendly project name generator."""

from __future__ import annotations

import random
import time

from ._mangle import join_clean, mangle
from ._wordlist import COMMON, GEO

__version__ = "0.2.0"

__all__ = ["generate"]

def _pick_words(rng: random.Random) -> tuple[str, str]:
    """Return two raw lowercase words in a random order."""
    geo = rng.choice(GEO).lower()
    common = rng.choice(COMMON).lower()
    if rng.random() < 0.5:
        return geo, common
    return common, geo


def generate(seed: int | None = None) -> str:
    """Generate a fun project name.

    Picks two words, fuses them with junction cleanup, applies consonant
    rotation, and capitalizes the first letter.
    """
    if seed is None:
        seed = time.time_ns()
    rng = random.Random(seed)

    a, b = _pick_words(rng)
    fused = join_clean(a, b)
    rotated = mangle(fused)
    return rotated[:1].upper() + rotated[1:]
