#
# Лабораторная работа №3 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентом группы 421702 БГУИР Евик Алексей Николаевич
#
#
# Сборка программы прямого нечёткого вывода (fuzzy_inference) и тестов (fuzzy_tests).
# Папка examples копируется в каталог сборки, чтобы из IDE работали пути вида examples/01_reference.txt.
# Использованные материалы - CMake Documentation - URL: https://cmake.org/cmake/help/latest/
#     (дата обращения: 13.10.2026)
# Версия 2.0 (13.10.2026): упрощённая версия программы (src/fuzzy.h, src/parser.cpp, src/inference.cpp).
#
cmake_minimum_required(VERSION 3.16)
project(FuzzyInference LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/utf-8 /W4)  # исходники в UTF-8 (русский текст в консоли)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

add_library(fuzzy_core STATIC src/parser.cpp src/inference.cpp)
target_include_directories(fuzzy_core PUBLIC src)

add_executable(fuzzy_inference src/main.cpp)
target_link_libraries(fuzzy_inference PRIVATE fuzzy_core)

if(EXISTS ${PROJECT_SOURCE_DIR}/examples)
    file(COPY ${PROJECT_SOURCE_DIR}/examples DESTINATION ${PROJECT_BINARY_DIR})
endif()

if(EXISTS ${PROJECT_SOURCE_DIR}/tests/tests.cpp)
    add_executable(fuzzy_tests tests/tests.cpp)
    target_link_libraries(fuzzy_tests PRIVATE fuzzy_core)
    enable_testing()
    add_test(NAME unit_tests COMMAND fuzzy_tests)
endif()