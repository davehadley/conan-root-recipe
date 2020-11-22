cmake_minimum_required(VERSION 3.18.4)
project(PackageTest CXX)

find_package(Catch2 REQUIRED)
include_directories(${Catch2_INCLUDE_DIRS})

find_package(root REQUIRED)
find_package(ROOT REQUIRED)
include(${ROOT_USE_FILE})

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
ROOT_GENERATE_DICTIONARY(G__Event Particle.hpp Event.hpp LINKDEF EventLinkDef.h)

add_library(Event SHARED Particle.cpp Event.cpp G__Event.cxx)
target_link_libraries(Event ${ROOT_LIBRARIES})

add_executable(example example.cpp)
target_link_libraries(example Event root::root)

install(TARGETS example)

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
