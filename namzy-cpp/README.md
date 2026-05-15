# namzy-cpp

A C++/Qt5 CLI tool that generates fun, human-friendly project names.

## Dependencies

- Qt 5.15+ (Core and Network modules)
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
./build/namzy                          # single word (offline, default)
./build/namzy --shape joined           # TwoWordPascal
./build/namzy --shape spaced           # Two Word
./build/namzy --shape spaced --count 5 # five spaced names
./build/namzy --online                 # fetch words from public API
./build/namzy --seed 12345             # reproducible output
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--shape single\|joined\|spaced` | `single` | Output format |
| `--online` | off | Fetch words from random-word-api |
| `--count N` | `1` | Number of names to generate |
| `--seed N` | timestamp | RNG seed for reproducibility |

## Notes

- Offline mode uses a bundled wordlist (~40 geographic + ~40 common words).
- Online mode hits `https://random-word-api.herokuapp.com/word?number=2&length=6` with a 3-second timeout and falls back to offline on failure.
- A light phonetic mangling pass is applied (e.g. `Boys→Boyz`, `ks→x`, `ph→f`).
