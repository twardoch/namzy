# this_file: src/namzy/__init__.py
"""namzy — compact, memorable, unique project name generator."""

from __future__ import annotations

import random
import time

from ._mangle import apply_rotations, build_name
from ._wordlist import ROTATIONS, STEMS

try:
    from .__version__ import __version__
except ModuleNotFoundError:
    __version__ = "0+unknown"

__all__ = [
    "generate",
    "generate_many",
    "apply_rotations",
    "build_name",
    "STEMS",
    "ROTATIONS",
    "__version__",
]


def generate(seed: int | None = None) -> str:
    """Generate a single name. Seed defaults to current time."""
    if seed is None:
        seed = time.time_ns()
    return build_name(random.Random(seed))


def generate_many(count: int, seed: int | None = None) -> list[str]:
    """Generate `count` names with seeds derived from `seed`."""
    base = time.time_ns() if seed is None else seed
    return [generate(base + i) for i in range(count)]
