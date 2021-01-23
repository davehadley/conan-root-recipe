cmake_minimum_required(VERSION 3.9)
project(cmake_wrapper)

include(conanbuildinfo)
#conan_basic_setup()

# sets the current C runtime on MSVC (MT vs MD vd MTd vs MDd)
conan_set_vs_runtime()

# Conan generated cmake_find_packages names differ from
# names ROOT expects (usually only due to case differences)
# There is currently no way to change these names
# see: https://github.com/conan-io/conan/issues/4430
find_package(OpenSSL REQUIRED)
set(OPENSSL_VERSION ${OpenSSL_VERSION})
find_package(LibXml2 REQUIRED)
set(LIBXML2_INCLUDE_DIR ${LibXml2_INCLUDE_DIR})
set(LIBXML2_LIBRARIES ${LibXml2_LIBRARIES})
find_package(SQLite3 REQUIRED)
set(SQLITE_INCLUDE_DIR ${SQLITE3_INCLUDE_DIRS})
set(SQLITE_LIBRARIES SQLite::SQLite3)

# add_subdirectory(ROOT SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder")
include(ExternalProject)
ExternalProject_Add(ROOT SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder")