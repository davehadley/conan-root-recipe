cmake_minimum_required(VERSION 3.13)
project(PackageTest CXX)

find_package(ROOT REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
ROOT_GENERATE_DICTIONARY(G__Event Event.hpp OPTIONS -inlineInputHeader LINKDEF EventLinkDef.h )

add_library(Event SHARED Event.cpp G__Event.cxx)
target_link_libraries(Event ROOT::ROOT)

add_executable(testrootdictionaries testrootdictionaries.cpp)
target_link_libraries(testrootdictionaries Event ROOT::ROOT)
