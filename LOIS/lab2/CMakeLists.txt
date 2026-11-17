cmake_minimum_required(VERSION 4.2)
project(lab2)

set(CMAKE_CXX_STANDARD 20)

add_executable(lab2 main.cpp
        parser.h
        parser.cpp
        inference.h
        inference.cpp)
