import os
import stat
from contextlib import contextmanager
from glob import glob
from tempfile import TemporaryDirectory
from typing import List

from conans import CMake, ConanFile, tools


class PythonOption:
    OFF = "off"
    SYSTEM = "system"
    # in future we may allow the user to specify a version when
    # libPython is available in Conan Center Index.
    ALL = [OFF, SYSTEM]
    DEFAULT = OFF


class RootConan(ConanFile):
    name = "root"
    version = "v6-22-02"
    license = "LGPL-2.1-or-later"  # of ROOT itself, the recipe is under MIT license.
    homepage = "https://root.cern/"
    # ROOT itself is located at: https://github.com/root-project/root
    url = "https://github.com/conan-io/conan-center-index"
    description = "CERN ROOT data analysis framework."
    topics = ("data-analysis", "physics")
    settings = ("os", "compiler", "build_type", "arch")
    options = {
        # don't allow static build as it is not supported
        # see: https://sft.its.cern.ch/jira/browse/ROOT-6446
        "shared": [True],
        "fPIC": [True, False],
        "python": PythonOption.ALL,
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "libxml2:shared": True,
        "sqlite3:shared": True,
        # default python=off as there is currently no libpython in Conan center
        "python": PythonOption.OFF,
    }
    generators = ("cmake_find_package",)
    requires = (
        "opengl/system",
        "libxml2/2.9.10",
        "glu/system",
        "xorg/system",
        "sqlite3/3.33.0",
        "libjpeg/9d",
        "libpng/1.6.37",
    )

    @property
    def _rootsrcdir(self) -> str:
        version = self.version.replace("v", "")
        return f"root-{version}"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        # Patch ROOT to use Conan SQLITE
        tools.replace_in_file(
            f"{self._rootsrcdir}{os.sep}CMakeLists.txt",
            "project(ROOT)",
            """project(ROOT)
            find_package(SQLite3 REQUIRED)
            set(SQLITE_INCLUDE_DIR ${SQLITE3_INCLUDE_DIRS})
            set(SQLITE_LIBRARIES SQLite::SQLite)
            """,
        )
        # Fix execute permissions on scripts
        scripts = [
            filename
            for pattern in ("**/configure", "**/*.sh", "**/*.csh", "**/*.bat")
            for filename in glob(pattern, recursive=True)
        ]
        for s in scripts:
            self._make_file_executable(s)

    def _make_file_executable(self, filename):
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)

    @contextmanager
    def _configure_cmake(self) -> CMake:
        with TemporaryDirectory() as cmakeinstalldir:
            cmake = CMake(self)
            version = self.version.replace("v", "")
            cmake.configure(
                source_folder=f"root-{version}",
                defs={
                    "fail-on-missing": "ON",
                    "CMAKE_CXX_STANDARD": self._CMAKE_CXX_STANDARD,
                    # Prefer builtins where available
                    "builtin_pcre": "ON",
                    "builtin_lzma": "ON",
                    "builtin_zstd": "ON",
                    "builtin_xxhash": "ON",
                    "builtin_lz4": "ON",
                    "builtin_afterimage": "ON",
                    "builtin_gsl": "ON",
                    "builtin_glew": "ON",
                    "builtin_gl2ps": "ON",
                    "builtin_openssl": "ON",
                    "builtin_fftw3": "ON",
                    "builtin_cfitsio": "ON",
                    "builtin_ftgl": "ON",
                    "builtin_davix": "ON",
                    "builtin_tbb": "ON",
                    "builtin_vdt": "ON",
                    # xrootd doesn't build with builtin openssl.
                    "builtin_xrootd": "OFF",
                    "xrootd": "OFF",
                    # No Conan packages available for these dependencies yet
                    "pythia6": "OFF",
                    "pythia8": "OFF",
                    "mysql": "OFF",
                    "oracle": "OFF",
                    "pgsql": "OFF",
                    "gfal": "OFF",
                    "tmva-pymva": "OFF",
                    "pyroot": self._pyrootopt,
                    "gnuinstall": "OFF",
                    "soversion": "ON",
                    # Tell CMake where to look for Conan provided depedencies
                    "CMAKE_LIBRARY_PATH": ";".join(self.deps_cpp_info.lib_paths),
                    "CMAKE_INCLUDE_PATH": ";".join(self.deps_cpp_info.include_paths),
                    # Configure install directories
                    # Conan CCI hooks restrict the allowed install directory
                    # names but ROOT is very picky about where build/runtime
                    # resources get installed.
                    # Set install directories to work around these limitations
                    # Following: https://github.com/conan-io/conan/issues/3695
                    "CMAKE_INSTALL_PREFIX": f"{self.package_folder}/res",
                    "CMAKE_INSTALL_INCLUDEDIR": "../include",
                    "CMAKE_INSTALL_BINDIR": "../bin",
                    "CMAKE_INSTALL_LIBDIR": "../lib",
                    "CMAKE_VERBOSE_MAKEFILE": "ON",
                },
            )
            yield cmake

    @property
    def _CMAKE_CXX_STANDARD(self):
        compileropt = self.settings.compiler.cppstd
        if compileropt:
            return str(compileropt)
        else:
            return "11"

    @property
    def _pyrootopt(self):
        if self.options.python == PythonOption.OFF:
            return "OFF"
        else:
            return "ON"

    def build(self):
        with self._configure_cmake() as cmake:
            cmake.build()

    def package(self):
        # ROOT CMake installs files that Conan center will not allow
        with self._configure_cmake() as cmake:
            cmake.install()
        self.copy("LICENSE.txt", dst="licenses")
        # self.copy("*.h", "include", "include", keep_path=True)
        # self.copy("*.hxx", "include", "include", keep_path=True)
        # self.copy("*.lib", "lib", "lib", keep_path=True)
        # self.copy("*.so", "lib", "lib", keep_path=True)
        # self.copy("*.a", "lib", "lib", keep_path=True)
        # self.copy("*.dylib", "lib", "lib", keep_path=True)
        # self.copy("*", "bin", "bin", keep_path=False)
        self.copy("ROOTUseFile.cmake", dst="res/cmake", src="")
        self.copy("RootMacros.cmake", dst="res/cmake", src="")
        self.copy("RootTestDriver.cmake", dst="res/cmake", src="")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "ROOT"
        self.cpp_info.names["cmake_find_package_multi"] = "ROOT"
        libs = tools.collect_libs(self)
        # special treatment for tbb (to handle issue https://github.com/conan-io/conan/issues/5428)
        libs = self._fix_tbb_libs(libs)
        print(f"DEBUG {libs}")
        # raise Exception
        self.cpp_info.libs = libs
        self.cpp_info.builddirs = ["res/cmake"]
        self.cpp_info.build_modules.extend(
            [
                "res/cmake/RootMacros.cmake",
                # "res/cmake/ROOTUseFile.cmake",
            ]
        )
        self.cpp_info.resdirs = ["res", "etc", "geom", "config", "cmake"]

    def _fix_tbb_libs(self, libs: List[str]) -> List[str]:
        return [(("lib" + name + ".so.2") if "tbb" in name else name) for name in libs]
