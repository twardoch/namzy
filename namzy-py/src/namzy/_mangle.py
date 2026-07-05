# this_file: src/namzy/_mangle.py
"""Build a name: pick two short stems, validate the junction, apply one rotation."""

from __future__ import annotations

import random

from ._wordlist import BAD_SEAMS, ROTATIONS, STEMS

_MAX_LEN = 12
_MAX_TRIES = 8


def _has_triple_letter(s: str) -> bool:
    """True if any letter repeats three times in a row (e.g. the ``aaa`` in ``sahaaardvark``)."""
    return any(s[i] == s[i - 1] == s[i - 2] for i in range(2, len(s)))


def _junction_ugly(compound: str, junction: int) -> bool:
    start = max(0, junction - 2)
    end = min(len(compound), junction + 2)
    win = compound[start:end]
    return any(seam in win for seam in BAD_SEAMS)


def apply_rotation(s: str, rng: random.Random) -> str:
    """Apply exactly one rotation at a randomly chosen matching position."""
    matches: list[tuple[int, str, str]] = []
    for i in range(len(s)):
        for src, dst in ROTATIONS:
            if s[i : i + len(src)] == src:
                matches.append((i, src, dst))
    if not matches:
        return s
    i, src, dst = matches[rng.randrange(len(matches))]
    return s[:i] + dst + s[i + len(src) :]


def build_name(rng: random.Random) -> str:
    best = ""
    for _ in range(_MAX_TRIES):
        a = rng.choice(STEMS)
        b = rng.choice(STEMS)
        compound = a + b
        # Reject compounds that are too long, stutter, or fuse into an ugly seam.
        if (
            len(compound) > _MAX_LEN
            or _has_triple_letter(compound)
            or _junction_ugly(compound, len(a))
        ):
            best = best or compound
            continue
        rotated = apply_rotation(compound, rng)
        return rotated[:1].upper() + rotated[1:]
    rotated = apply_rotation(best, rng)
    return rotated[:1].upper() + rotated[1:]
