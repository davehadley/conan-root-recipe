cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()

find_package(root REQUIRED)
find_package(ROOT REQUIRED)
include(${ROOT_USE_FILE})

add_executable(example example.cpp)
target_link_libraries(example root::root)

install(TARGETS example)

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
