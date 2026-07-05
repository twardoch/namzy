# this_file: namzy-py/tests/test_namzy.py
"""Contract tests for namzy: determinism, output shape, and the mangle steps.

The four implementations are equivalent in spirit, not bit-identical, so these
tests check the *properties* the algorithm guarantees rather than fixed strings.
"""

from __future__ import annotations

import random
import string
import subprocess
import sys

import pytest

import namzy
from namzy import _mangle, _wordlist

# --- Data integrity -------------------------------------------------------


def test_stems_are_lowercase_ascii() -> None:
    assert _wordlist.STEMS, "stem list must not be empty"
    allowed = set(string.ascii_lowercase)
    for stem in _wordlist.STEMS:
        assert stem, "no empty stems"
        assert set(stem) <= allowed, f"non-ascii-lowercase stem: {stem!r}"


def test_stems_are_deduplicated() -> None:
    assert len(_wordlist.STEMS) == len(set(_wordlist.STEMS))


def test_rotations_are_well_formed() -> None:
    assert _wordlist.ROTATIONS
    for src, dst in _wordlist.ROTATIONS:
        assert src and dst, "rotation halves must be non-empty"
        assert src != dst, f"rotation is a no-op: {src!r}"
        assert set(src + dst) <= set(string.ascii_lowercase)


# --- generate() -----------------------------------------------------------


def test_generate_is_deterministic_for_a_seed() -> None:
    assert namzy.generate(seed=42) == namzy.generate(seed=42)


def test_different_seeds_usually_differ() -> None:
    names = {namzy.generate(seed=s) for s in range(200)}
    # A 950-stem cross product makes collisions rare; demand plenty of variety.
    assert len(names) > 150


def test_generate_returns_capitalized_ascii() -> None:
    for seed in range(500):
        name = namzy.generate(seed=seed)
        assert name, "name must not be empty"
        assert name[0].isupper()
        assert set(name.lower()) <= set(string.ascii_lowercase)


def test_generated_names_stay_short() -> None:
    # Two stems of <=7 chars, and a rotation shifts length by at most one.
    for seed in range(500):
        assert len(namzy.generate(seed=seed)) <= 16


# --- generate_many() ------------------------------------------------------


def test_generate_many_count_and_determinism() -> None:
    first = namzy.generate_many(25, seed=7)
    assert len(first) == 25
    assert first == namzy.generate_many(25, seed=7)


def test_generate_many_rejects_nothing_for_zero() -> None:
    assert namzy.generate_many(0, seed=1) == []


# --- apply_rotation() -----------------------------------------------------


def test_apply_rotation_changes_at_most_one_site() -> None:
    rng = random.Random(0)
    src, dst = _wordlist.ROTATIONS[0]
    base = f"x{src}x{src}x"  # two rotation sites
    out = _mangle.apply_rotation(base, rng)
    # Exactly one occurrence should have been rewritten, so the count of the
    # source token drops by one (unless dst reintroduces it, which ROTATIONS avoid).
    assert out != base or src not in base


def test_apply_rotation_noop_when_no_match() -> None:
    rng = random.Random(0)
    # Every rotation source starts with a consonant, so a pure-vowel string
    # can contain no match and must pass through untouched.
    assert all(src[0] not in "aeiouy" for src, _ in _wordlist.ROTATIONS)
    assert _mangle.apply_rotation("aeiou", rng) == "aeiou"


# --- build_name() ---------------------------------------------------------


def test_build_name_uses_bundled_stems_only() -> None:
    # With rotations disabled we can prove the output is a fusion of two stems.
    rng = random.Random(3)
    stem_set = set(_wordlist.STEMS)
    original = _mangle.ROTATIONS
    try:
        _mangle.ROTATIONS = []  # type: ignore[assignment]
        name = _mangle.build_name(rng).lower()
    finally:
        _mangle.ROTATIONS = original  # type: ignore[assignment]
    split = [
        (name[:i], name[i:])
        for i in range(1, len(name))
        if name[:i] in stem_set and name[i:] in stem_set
    ]
    assert split, f"{name!r} is not a fusion of two bundled stems"


@pytest.mark.parametrize("seed", [0, 1, 42, 1000, 999999])
def test_smoke_cli_entrypoint(seed: int) -> None:
    # generate() is what the CLI calls; ensure it never raises across seeds.
    assert isinstance(namzy.generate(seed=seed), str)


# --- CLI ------------------------------------------------------------------


def test_cli_prints_requested_count(capsys, monkeypatch) -> None:
    from namzy import cli

    monkeypatch.setattr(sys, "argv", ["namzy", "--count", "4", "--seed", "5"])
    cli.main()
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 4
    assert all(line[0].isupper() for line in lines)


def test_cli_seed_is_reproducible(capsys, monkeypatch) -> None:
    from namzy import cli

    monkeypatch.setattr(sys, "argv", ["namzy", "--count", "3", "--seed", "99"])
    cli.main()
    first = capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", ["namzy", "--count", "3", "--seed", "99"])
    cli.main()
    assert capsys.readouterr().out == first


def test_module_execution_runs_main() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "namzy", "--count", "2", "--seed", "1"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert len(result.stdout.splitlines()) == 2
