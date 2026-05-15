# this_file: src/namzy/cli.py
"""CLI entrypoint for namzy."""

from __future__ import annotations

import argparse
import time

from . import generate


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="namzy",
        description="Generate fun human-friendly project names.",
    )
    parser.add_argument(
        "--online",
        action="store_true",
        default=False,
        help="Fetch words from a public API (falls back to offline on error)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        metavar="N",
        help="Number of names to generate (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        metavar="INT",
        help="Random seed for reproducible output",
    )

    args = parser.parse_args()

    base_seed = args.seed if args.seed is not None else time.time_ns()

    for i in range(args.count):
        print(generate(online=args.online, seed=base_seed + i))
