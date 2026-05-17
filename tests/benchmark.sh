#!/usr/bin/env bash
# this_file: tests/benchmark.sh
# Generate 10,000 names per implementation into tests/output/ and report timings.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/tests/output"
mkdir -p "$OUT"

N=10000
SEED=1

echo "Generating $N names per implementation (seed=$SEED)..."
echo

bench() {
    local name="$1"; shift
    local out="$OUT/$name.txt"
    local start end ms
    start=$(python3 -c 'import time; print(time.perf_counter_ns())')
    "$@" > "$out"
    end=$(python3 -c 'import time; print(time.perf_counter_ns())')
    ms=$(( (end - start) / 1000000 ))
    local lines
    lines=$(wc -l < "$out" | tr -d ' ')
    local uniq
    uniq=$(sort -u "$out" | wc -l | tr -d ' ')
    printf "  %-8s  %6d ms   lines=%s  unique=%s\n" "$name" "$ms" "$lines" "$uniq"
}

bench ts  node     "$ROOT/namzy-ts/dist/cli.js"        --count $N --seed $SEED
bench py  python3 -c "
import sys
sys.path.insert(0, '$ROOT/namzy-py/src')
from namzy import generate_many
print('\n'.join(generate_many($N, seed=$SEED)))
"
bench rs  "$ROOT/namzy-rs/target/release/namzy"        --count $N --seed $SEED
bench cpp "$ROOT/namzy-cpp/build/namzy"                --count $N --seed $SEED

echo
echo "Sample output (cpp):"
head -10 "$OUT/cpp.txt"
