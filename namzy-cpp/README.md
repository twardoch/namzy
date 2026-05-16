# namzy-cpp

A C++/Qt5 CLI tool that generates fun, human-friendly project names.

## Dependencies

- Qt 5.15+ (Core module)
- CMake 3.16+
- A C++17-capable compiler

On macOS: `brew install qt@5`
On Ubuntu: `sudo apt install qt5-default`

## Build

```sh
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/Qt5
cmake --build build
```

If Qt5 is on your PATH (e.g. via `brew link qt@5`), you can omit `CMAKE_PREFIX_PATH`:

```sh
cmake -S . -B build && cmake --build build
```

## Usage

```sh
./build/namzy                          # one fused name
./build/namzy --count 5                # five names
./build/namzy --seed 12345             # reproducible output
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--count N` | `1` | Number of names to generate |
| `--seed N` | timestamp | RNG seed for reproducibility |

## Notes

- Namzy uses the shared bundled wordlists of 500 geographic names and 500 common words. Each pair may be joined in either order, for 500,000 raw ordered pairings before seam cleanup and replacement collisions.
- Seam cleanup runs first, then each name activates a seed-derived subset of 1 to 10 replacement rules from `c→q · f→v · k→c · q→k · s→z · z→s · v→f · w→u · b→p · p→b`.
