#!/usr/bin/env bash
# Build all namzy packages.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; RESET=$'\033[0m'
say() { printf "%s==> %s%s\n" "$GREEN" "$1" "$RESET"; }
warn() { printf "%s--- %s%s\n" "$YELLOW" "$1" "$RESET"; }
die() { printf "%sxxx %s%s\n" "$RED" "$1" "$RESET" >&2; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }

# --- TypeScript -----------------------------------------------------------
say "Building namzy-ts (npm)"
pushd namzy-ts >/dev/null
  have npm || die "npm not found"
  npm install --no-audit --no-fund
  npm run build
  npm run build:web
popd >/dev/null

# --- Python ---------------------------------------------------------------
say "Building namzy-py (wheel + sdist)"
pushd namzy-py >/dev/null
  if have uv; then
    uv build
  elif have python3; then
    python3 -m pip install --quiet --upgrade build
    python3 -m build
  else
    die "Neither uv nor python3 found"
  fi
popd >/dev/null

# --- Rust -----------------------------------------------------------------
say "Building namzy-rs (cargo release)"
pushd namzy-rs >/dev/null
  have cargo || die "cargo not found"
  cargo build --release
  cargo package --allow-dirty --no-verify >/dev/null
popd >/dev/null

# --- C++ ------------------------------------------------------------------
say "Building namzy-cpp (cmake)"
pushd namzy-cpp >/dev/null
  if have cmake; then
    EXTRA=()
    if [[ -d /opt/homebrew/opt/qt@5 ]]; then
      EXTRA+=(-DCMAKE_PREFIX_PATH=/opt/homebrew/opt/qt@5)
    elif [[ -d /usr/local/opt/qt@5 ]]; then
      EXTRA+=(-DCMAKE_PREFIX_PATH=/usr/local/opt/qt@5)
    fi
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release "${EXTRA[@]}"
    cmake --build build --parallel
  else
    warn "cmake not found — skipping C++ build"
  fi
popd >/dev/null

say "All builds done."
