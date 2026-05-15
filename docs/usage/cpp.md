---
title: C++ / Qt 5
permalink: /usage/cpp/
nav_order: 4
---

# C++ / Qt 5

The C++ implementation lives in `namzy-cpp`. It is a Qt 5 project that links against Qt Core and Qt Network.

## Build

From the repository root:

```bash
cmake -S namzy-cpp -B namzy-cpp/build
cmake --build namzy-cpp/build
```

If CMake cannot find Qt 5, pass `CMAKE_PREFIX_PATH`:

```bash
cmake -S namzy-cpp -B namzy-cpp/build -DCMAKE_PREFIX_PATH=/path/to/Qt/5.x/clang_64
cmake --build namzy-cpp/build
```

The project uses C++17 and enables Qt automoc.

## CLI

After building, run the executable from the build directory:

```bash
namzy-cpp/build/namzy --count 5
```

With a deterministic seed:

```bash
namzy-cpp/build/namzy --count 5 --seed 42
```

With online source words:

```bash
namzy-cpp/build/namzy --online --count 5
```

CLI flags:

| Flag | Description |
| --- | --- |
| `--count N` | Print `N` names. Defaults to `1`. |
| `--seed N` | Seed the generator. |
| `--online` | Try online source words before falling back to bundled wordlists. |

## Use from Qt 5 code

Include `namzy.h` and link the implementation files into your Qt target.

```cpp
#include "namzy.h"

Namzy generator(42);

QString offline = generator.generateOffline();
QString online = generator.generateOnline();
```

`generateOffline()` uses bundled wordlists. `generateOnline()` uses `QNetworkAccessManager` to request source words from the public random-word API, then falls back to offline generation if the request fails or times out.

## CMake embedding example

```cmake
find_package(Qt5 COMPONENTS Core Network REQUIRED)

add_executable(my_app
  main.cpp
  ../namzy-cpp/src/namzy.cpp
  ../namzy-cpp/src/mangle.cpp
  ../namzy-cpp/src/wordlist.cpp
)

target_include_directories(my_app PRIVATE ../namzy-cpp/src)
target_link_libraries(my_app PRIVATE Qt5::Core Qt5::Network)
```
