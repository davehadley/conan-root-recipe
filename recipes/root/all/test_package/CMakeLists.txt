cmake_minimum_required(VERSION 3.13)
project(PackageTest CXX)

set(CMAKE_INSTALL_RPATH $ORIGIN)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(ROOT REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
ROOT_GENERATE_DICTIONARY(G__Event Particle.hpp Event.hpp OPTIONS -inlineInputHeader LINKDEF EventLinkDef.h )

add_library(Event SHARED Particle.cpp Event.cpp G__Event.cxx)
#add_library(Event SHARED Particle.cpp Event.cpp)
target_link_libraries(Event ROOT::ROOT)

add_executable(testrootio testrootio.cpp)
target_link_libraries(testrootio Event ROOT::ROOT)


include(GNUInstallDirs)
install(TARGETS testrootio
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
