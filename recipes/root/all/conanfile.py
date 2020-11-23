import os

from conans import CMake, ConanFile, tools


class PythonSetting:
    OFF = "off"
    SYSTEM = "system"
    # in future we may allow the user to specify a version...

    ALL = [OFF, SYSTEM]
    DEFAULT = OFF


class RootConan(ConanFile):
    name = "root"
    version = "v6-22-02"
    license = (
        "LGPL-2.1-or-later"  # of ROOT itself, the conan recipe is under MIT license.
    )
    homepage = "https://root.cern/"
    url = "https://github.com/davehadley/conan-root-recipe"  # ROOT itself is located at: https://github.com/root-project/root
    description = "CERN ROOT data analysis framework."
    topics = ("data-analysis", "physics")
    settings = ("os", "compiler", "build_type", "arch")
    options = {"shared": [True, False], "python": PythonSetting.ALL}
    default_options = {
        "shared": True,
        "libxml2:shared": True,
        "sqlite3:shared": True,
        # default pyroot to off as there is currently no libpython in conan center index
        "python": PythonSetting.ALL,
    }
    generators = "cmake_find_package"
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
        tools.get(**self.conan_data["sources"][self.version], keep_permissions=True)
        tools.replace_in_file(
            f"{self._rootsrcdir}{os.sep}CMakeLists.txt",
            "project(ROOT)",
            """project(ROOT)
            find_package(SQLite3 REQUIRED)
            set(SQLITE_INCLUDE_DIR ${SQLITE3_INCLUDE_DIRS})
            set(SQLITE_LIBRARIES SQLite::SQLite)
            """,
        )

    def _configure_cmake(self) -> CMake:
        cmake = CMake(self)
        version = self.version.replace("v", "")
        cmake.configure(
            source_folder=f"root-{version}",
            defs={
                "fail-on-missing": "ON",
                "CMAKE_CXX_STANDARD": str(self.settings.compiler.cppstd),  # type: ignore
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
                "pyroot": "OFF"
                if self.options["pyroot"] == PythonSetting.OFF
                else "ON",
                # Tell CMake where to look for Conan provided depedencies
                "CMAKE_LIBRARY_PATH": ";".join(self.deps_cpp_info.lib_paths),
                "CMAKE_INCLUDE_PATH": ";".join(self.deps_cpp_info.include_paths),
                # "CMAKE_VERBOSE_MAKEFILE": "ON",
            },
        )
        return cmake

    def build(self):
        self._configure_cmake().build()

    def package(self):
        self._configure_cmake().install()

    def _getalllibs(self, dep: str) -> str:
        return ";".join(
            self.deps_cpp_info[dep].libs + self.deps_cpp_info[dep].system_libs
        )

    def _getincludeopt(self, depname: str) -> str:
        return ";".join(self.deps_cpp_info[depname].include_paths)

    def package_info(self):
        # get this list with root-config --libs
        self.cpp_info.names["cmake_find_package"] = "ROOT"
        self.cpp_info.libs = tools.collect_libs(self)
        # self.cpp_info.libs = [
        #     "Core",
        #     "Imt",
        #     "RIO",
        #     "Net",
        #     "Hist",
        #     "Graf",
        #     "Graf3d",
        #     "Gpad",
        #     "ROOTVecOps",
        #     "Tree",
        #     "TreePlayer",
        #     "Rint",
        #     "Postscript",
        #     "Matrix",
        #     "Physics",
        #     "MathCore",
        #     "Thread",
        #     "MultiProc",
        #     "ROOTDataFrame",
        #     "tbb",
        #     "vdt",
        # ]
