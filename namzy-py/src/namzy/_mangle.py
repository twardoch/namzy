# this_file: src/namzy/_mangle.py
"""Consonant-rotation mangling and word-junction cleanup."""

from __future__ import annotations

import random
from collections.abc import Iterable

_ROT = (
    ("c", "q"),
    ("f", "v"),
    ("k", "c"),
    ("q", "k"),
    ("s", "z"),
    ("z", "s"),
    ("v", "f"),
    ("w", "u"),
    ("b", "p"),
    ("p", "b"),
)
_ALL_RULES = frozenset(range(len(_ROT)))
_VOWELS = frozenset("aeiouy")


def active_rotation_rules(rng: random.Random) -> frozenset[int]:
    """Choose 1..10 active consonant-rotation rules from the seeded RNG."""
    count = rng.randrange(1, len(_ROT) + 1)
    return frozenset(rng.sample(range(len(_ROT)), count))


def _rot_char(ch: str, active_rules: frozenset[int]) -> str:
    low = ch.lower()
    for idx, (src, dst) in enumerate(_ROT):
        if idx in active_rules and low == src:
            return dst.upper() if ch.isupper() else dst
    return ch


def mangle(s: str, active_rules: Iterable[int] | None = None) -> str:
    """Apply case-preserving consonant rotation.

    If no rule subset is provided, all rules are active for direct helper use.
    """
    active = _ALL_RULES if active_rules is None else frozenset(active_rules)
    return "".join(_rot_char(c, active) for c in s)


def join_clean(a: str, b: str) -> str:
    """Fuse two raw lowercase words, smoothing the junction.

    Up to two passes: drop first char of tail if it duplicates the last char
    of head (case-insensitive), or if both are vowels.
    """
    head = a
    tail = b
    for _ in range(2):
        if not head or not tail:
            break
        h = head[-1].lower()
        t = tail[0].lower()
        if h == t:
            tail = tail[1:]
        elif h in _VOWELS and t in _VOWELS:
            tail = tail[1:]
        else:
            break
    return head + tail
