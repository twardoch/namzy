---
title: C++ / Qt 5
permalink: /usage/cpp-qt5/
description: Build and embed the C++ implementation, including Qt 5 applications.
parent: Usage
nav_order: 4
---

The C++ implementation lives in `namzy-cpp/`. It is Qt 5-compatible and uses Qt Core plus Qt Network.

## Build the CLI

```bash
git clone https://github.com/twardoch/namzy.git
cd namzy/namzy-cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/namzy --count 5
```

If CMake cannot find Qt 5, pass your Qt installation path:

```bash
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/Qt/5.x/clang_64
```

## CLI

```bash
./build/namzy --count 5
./build/namzy --seed 42 --count 3
./build/namzy --online --count 3
```

CLI options:

- `--count N`: print `N` names, default `1`.
- `--seed N`: seed the offline generator.
- `--online`: request random source words before falling back to bundled words.

## Embed in a Qt 5 app

Add the implementation files to your Qt target and link Qt Core and Qt Network:

```cmake
find_package(Qt5 COMPONENTS Core Network REQUIRED)

add_executable(myapp
  main.cpp
  path/to/namzy.cpp
  path/to/mangle.cpp
  path/to/wordlist.cpp
)

target_include_directories(myapp PRIVATE path/to/namzy-cpp/src)
target_link_libraries(myapp PRIVATE Qt5::Core Qt5::Network)
```

Then call `Namzy` from C++:

```cpp
#include "namzy.h"
#include <QDebug>

int main() {
    Namzy generator(42);

    const QString offline = generator.generateOffline();
    qDebug() << offline;

    const QString online = generator.generateOnline();
    qDebug() << online;
}
```

`generateOnline()` performs a short Qt Network request to the public random-word API and falls back to `generateOffline()` if the request times out, fails, or returns invalid words.
