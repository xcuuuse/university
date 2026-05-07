cmake_minimum_required(VERSION 4.2)
project(lab1)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++ -static")
add_executable(lab1 src/main.cpp
        src/node/node.h
        src/node/node.cpp
        src/parser/parser.h
        src/parser/parser.cpp
)
target_include_directories(lab1 PRIVATE ${CMAKE_SOURCE_DIR}/src)
