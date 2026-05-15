# this_file: src/namzy/_mangle.py
"""Consonant-rotation mangling and word-junction cleanup."""

from __future__ import annotations

_ROT = {
    "c": "q",
    "f": "v",
    "k": "c",
    "q": "k",
    "s": "z",
    "z": "s",
    "v": "f",
    "w": "u",
}

_VOWELS = frozenset("aeiouy")


def _rot_char(ch: str) -> str:
    low = ch.lower()
    if low in _ROT:
        sub = _ROT[low]
        return sub.upper() if ch.isupper() else sub
    return ch


def mangle(s: str) -> str:
    """Apply per-letter consonant rotation, case-preserving."""
    return "".join(_rot_char(c) for c in s)


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
