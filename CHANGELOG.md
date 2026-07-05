# Changelog

All notable changes to namzy are recorded here. The project versions all four
implementations in lockstep from a single `vX.Y.Z` git tag.

## [Unreleased]

### Added
- Contract test suites for the three publishable implementations, asserting the
  algorithm's guarantees (determinism, capitalized ASCII output, length bound,
  seam rejection, single-rotation behavior) rather than fixed strings:
  - `namzy-py/tests/test_namzy.py` — 20 pytest cases, 87% line coverage.
  - `namzy-rs/tests/contract.rs` — 6 integration tests.
  - `namzy-ts/test/namzy.test.ts` — 6 `node:test` cases; new `test` and
    `typecheck` npm scripts.
- GitHub Actions `ci.yml`: lint, type-check, and test every implementation
  (Python, TypeScript, Rust) plus a Qt5 C++ build on every push and PR.
- GitHub Actions `release.yml`: on a `vX.Y.Z` tag, sync versions, build all
  packages, publish to PyPI / npm / crates.io when the matching token secret is
  set, and cut a GitHub release.
- Ruff, mypy (strict), pytest, and coverage configuration in `namzy-py`.

### Changed
- Rewrote the README "Shared contract" section to describe the algorithm the
  code actually runs (stem fusion, bad-seam rejection, one syllable rotation)
  and refreshed the example names to authentic output.
- Documented the `fit` and `unified` stem-list helpers in
  `scripts/generate_data.py`.

### Fixed
- `namzy-py/src/namzy/__version__.py` is now tracked instead of gitignored, so
  a fresh checkout resolves the hatch version and builds/tests without first
  running `scripts/sync_version.py` — this unblocks CI.
