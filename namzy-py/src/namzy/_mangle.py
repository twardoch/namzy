# this_file: src/namzy/_mangle.py
"""Build one name: pick two stems, concatenate, lightly rotate, capitalize."""

from __future__ import annotations

import random

from ._wordlist import ROTATIONS, STEMS

_ROT_MAP: dict[str, str] = dict(ROTATIONS)


def _rotate_at(s: str, pos: int) -> str:
    ch = s[pos]
    low = ch.lower()
    repl = _ROT_MAP.get(low)
    if repl is None:
        return s
    out = repl.upper() if ch.isupper() else repl
    return s[:pos] + out + s[pos + 1:]


def apply_rotations(compound: str, rng: random.Random) -> str:
    """Apply 1 or 2 rotations on randomly selected positions."""
    if not compound:
        return compound
    passes = 1 if rng.random() < 0.5 else 2
    out = compound
    for _ in range(passes):
        out = _rotate_at(out, rng.randrange(len(out)))
    return out


def build_name(rng: random.Random) -> str:
    a = rng.choice(STEMS)
    b = rng.choice(STEMS)
    rotated = apply_rotations(a + b, rng)
    return rotated[:1].upper() + rotated[1:]
