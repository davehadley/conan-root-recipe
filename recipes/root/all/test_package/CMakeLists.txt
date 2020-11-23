cmake_minimum_required(VERSION 3.13)
project(PackageTest CXX)


include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(Catch2 REQUIRED)
include_directories(${Catch2_INCLUDE_DIRS})

find_package(ROOT REQUIRED)
include(${ROOT_USE_FILE})

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
ROOT_GENERATE_DICTIONARY(G__Event Particle.hpp Event.hpp OPTIONS -inlineInputHeader LINKDEF EventLinkDef.h )

add_library(Event SHARED Particle.cpp Event.cpp G__Event.cxx)
# target_link_libraries(Event)

add_executable(example_targets example.cpp)
target_link_libraries(example_targets Event ROOT::Core ROOT::Hist ROOT::Tree ROOT::Physics ROOT::Thread)

add_executable(example_vars example.cpp)
target_link_libraries(example_vars Event ${ROOT_LIBRARIES})

include(GNUInstallDirs)
install(TARGETS example_targets example_vars
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)


# CTest is a testing tool that can be used to test your project.
# enable_testing()
add_test(NAME example_targets
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
         COMMAND example_targets)

add_test(NAME example_vars
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
         COMMAND example_vars)