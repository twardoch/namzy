#!/usr/bin/env bash
# Publish all namzy packages to their respective registries.
# Usage: ./publish.sh [--dry-run]
#
# TS  → npm     (needs `npm login`)
# Py  → PyPI    (needs PYPI_TOKEN env or `~/.pypirc`)
# Rs  → crates  (needs `cargo login`)
# C++ →         (not published — built only)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

DRY=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY="1"
fi

GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; RESET=$'\033[0m'
say() { printf "%s==> %s%s\n" "$GREEN" "$1" "$RESET"; }
warn() { printf "%s--- %s%s\n" "$YELLOW" "$1" "$RESET"; }
die() { printf "%sxxx %s%s\n" "$RED" "$1" "$RESET" >&2; exit 1; }
run() {
  if [[ -n "$DRY" ]]; then
    printf "%s[dry-run]%s %s\n" "$YELLOW" "$RESET" "$*"
  else
    "$@"
  fi
}

have() { command -v "$1" >/dev/null 2>&1; }

assert_clean_except_rust_version_files() {
  local status path
  while IFS= read -r status; do
    [[ -z "$status" ]] && continue
    path="${status:3}"
    case "$path" in
      namzy-rs/Cargo.toml|namzy-rs/Cargo.lock) ;;
      *) die "Refusing cargo publish with unexpected dirty Rust package file: $path" ;;
    esac
  done < <(git status --porcelain -- namzy-rs)
}

version_from_gitnextver() {
  if [[ -n "${NAMZY_VERSION:-}" ]]; then
    printf "%s\n" "$NAMZY_VERSION"
    return
  fi
  have uvx || die "uvx not found; install uv or set NAMZY_VERSION=vX.Y.Z"
  uvx gitnextver
}

say "Synchronizing package versions"
VERSION_TAG="$(version_from_gitnextver)"
NAMZY_VERSION="$VERSION_TAG" python3 "$ROOT/scripts/sync_version.py" "$VERSION_TAG"
export NAMZY_VERSION="$VERSION_TAG"

# Build everything first so we publish from fresh artifacts.
say "Building all packages"
"$ROOT/build.sh"

# --- TypeScript → npm ----------------------------------------------------
say "Publishing namzy-ts → npm"
pushd namzy-ts >/dev/null
  have npm || die "npm not found"
  if [[ -n "$DRY" ]]; then
    npm publish --dry-run --access public
  else
    npm publish --access public
  fi
popd >/dev/null

# --- Python → PyPI -------------------------------------------------------
say "Publishing namzy-py → PyPI"
pushd namzy-py >/dev/null
  if have uv; then
    if [[ -n "$DRY" ]]; then
      warn "uv publish has no --dry-run; listing artifacts only"
      ls -la dist/
    else
      uv publish
    fi
  else
    have twine || python3 -m pip install --quiet --upgrade twine
    if [[ -n "$DRY" ]]; then
      python3 -m twine check dist/*
    else
      python3 -m twine upload dist/*
    fi
  fi
popd >/dev/null

# --- Rust → crates.io ----------------------------------------------------
say "Publishing namzy-rs → crates.io"
pushd namzy-rs >/dev/null
  have cargo || die "cargo not found"
  if [[ -n "$DRY" ]]; then
    cargo publish --dry-run --allow-dirty
  else
    assert_clean_except_rust_version_files
    cargo publish --allow-dirty
  fi
popd >/dev/null

# --- C++ -----------------------------------------------------------------
warn "namzy-cpp is not published — binary only"

say "All publishes done."
