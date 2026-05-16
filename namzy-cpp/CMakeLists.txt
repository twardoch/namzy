cmake_minimum_required(VERSION 3.16)
project(namzy VERSION 1.0.14 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt5 COMPONENTS Core REQUIRED)

add_executable(namzy
    src/main.cpp
    src/namzy.cpp
    src/wordlist.cpp
    src/mangle.cpp
)

target_link_libraries(namzy Qt5::Core)

target_compile_definitions(namzy PRIVATE NAMZY_VERSION="${PROJECT_VERSION}")
