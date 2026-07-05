# TODO

Bigger ideas beyond the current modernization pass. Flat list; move items to
`CHANGELOG.md` when done.

- [ ] Publish `namzy-cpp` artifacts (per-OS binaries) via the release workflow, or decide to keep it build-only and say so in its README.
- [ ] Add a cross-language parity check to CI: generate N names per impl and assert similar length + character-frequency distributions (statistical, not bit-identical), replacing the manual `tests/benchmark.sh`.
- [ ] Adopt `hatch-vcs` for `namzy-py` so the Python version derives straight from the git tag, and teach `scripts/sync_version.py` to skip Python — currently the version is stamped into a tracked `__version__.py` to keep all four languages in lockstep.
- [ ] Prune the stale Python branch in `scripts/sync_version.py` (its `from ._wordlist import COMMON, GEO` marker no longer matches the source).
- [ ] Implement the "online" vocabulary mode named in `INIT.md`, or drop that requirement from the spec — no implementation fetches a remote wordlist today.
- [ ] Expand the stem packs (currently ~955 stems) and add a `namzy --list-packs` option to show which disciplines are bundled.
