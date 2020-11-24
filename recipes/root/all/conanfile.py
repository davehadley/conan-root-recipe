import os
import shutil

from conans import CMake, ConanFile, tools


class PythonOption:
    OFF = "off"
    SYSTEM = "system"
    # in future we may allow the user to specify a version when
    # libPython is available in Conan package center
    ALL = [OFF, SYSTEM]
    DEFAULT = OFF


class RootConan(ConanFile):
    name = "root"
    license = (
        "LGPL-2.1-or-later"  # of ROOT itself, the Conan recipe is under MIT license.
    )
    homepage = "https://root.cern/"
    url = "https://github.com/conan-io/conan-center-index"  # ROOT itself is located at: https://github.com/root-project/root
    description = "CERN ROOT data analysis framework."
    topics = ("data-analysis", "physics")
    settings = ("os", "compiler", "build_type", "arch")
    options = {
        # don't allow static build as it is not supported (see: https://sft.its.cern.ch/jira/browse/ROOT-6446)
        "shared": [True],
        "fPIC": [True, False],
        "python": PythonOption.ALL,
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "libxml2:shared": True,
        "sqlite3:shared": True,
        # default pyroot to off as there is currently no libpython in conan center index
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
        tools.get(**self.conan_data["sources"][self.version], keep_permissions=True)
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

    def _configure_cmake(self) -> CMake:
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
                # Tell CMake where to look for Conan provided depedencies
                "CMAKE_LIBRARY_PATH": ";".join(self.deps_cpp_info.lib_paths),
                "CMAKE_INCLUDE_PATH": ";".join(self.deps_cpp_info.include_paths),
                # "CMAKE_VERBOSE_MAKEFILE": "ON",
            },
        )
        return cmake

    @property
    def _CMAKE_CXX_STANDARD(self):
        compileropt = self.settings.compiler.cppstd
        print(f"DEBUG {compileropt}, {type(compileropt)}")
        if compileropt:
            return str(compileropt)
        else:
            return "11"

    @property
    def _pyrootopt(self):
        if self.options["python"] == PythonOption.OFF:
            return "OFF"
        else:
            return "ON"

    def build(self):
        self._configure_cmake().build()

    def package(self):
        self._configure_cmake().install()
        os.makedirs("licenses", exist_ok=True)
        shutil.move("LICENSE", "licenses")
        os.makedirs("res", exist_ok=True)
        for path in [
            "emacs",
            "man",
            "etc",
            "geom",
            "icons",
            "fonts",
            "js",
            "macros",
            "README",
            "tutorials",
        ]:
            shutil.move("path", "res")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "ROOT"
        self.cpp_info.names["cmake_find_package_multi"] = "ROOT"
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.builddirs = ["cmake"]
