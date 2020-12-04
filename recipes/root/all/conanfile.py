import os
import stat
from contextlib import contextmanager
from glob import glob
from typing import List

from conans import CMake, ConanFile, tools
from conans.errors import ConanInvalidConfiguration


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
        # Don't allow static build as it is not supported
        # see: https://sft.its.cern.ch/jira/browse/ROOT-6446
        # TODO: shared option should be reinstated when hooks issue is resolved
        # (see: https://github.com/conan-io/hooks/issues/252)
        # "shared": [True],
        "fPIC": [True, False],
        "python": PythonOption.ALL,
    }
    default_options = {
        # "shared": True,
        "fPIC": True,
        # "libxml2:shared": True,
        # "sqlite3:shared": True,
        # "zlib:shared": True,
        # default python=off as there is currently no libpython in Conan center
        "python": PythonOption.OFF,
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
        "libcurl/7.73.0",
        "pcre/8.44",
        "xz_utils/5.2.5",
        "zstd/1.4.5",
        "lz4/1.9.3",
        "glew/2.1.0",
        "openssl/1.1.1h",
        "fftw/3.3.8",
        "cfitsio/3.490",
        "tbb/2020.3",
        # "libuuid/1.0.3",
        # "freetype/2.10.4",
        "libpng/1.6.37",
        # "zlib/1.2.11",
    )

    def __init__(self, *args, **kwargs):
        super(RootConan, self).__init__(*args, **kwargs)
        self._cmake = None

    @property
    def _minimum_cpp_standard(self):
        return 11

    @property
    def _minimum_compilers_version(self):
        return {
            "Visual Studio": "16.1",
            "gcc": "4.8",
            "clang": "3.4",
            "apple-clang": "5.1",
        }

    @property
    def _rootsrcdir(self) -> str:
        version = self.version.replace("v", "")
        return f"root-{version}"

    def configure(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, self._minimum_cpp_standard)
        min_version = self._minimum_compilers_version.get(str(self.settings.compiler))
        if not min_version:
            self.output.warn(
                "{} recipe lacks information about the {} compiler support.".format(
                    self.name, self.settings.compiler
                )
            )
        else:
            if tools.Version(self.settings.compiler.version) < min_version:
                raise ConanInvalidConfiguration(
                    "{} requires C++{} support. The current compiler {} {} does not support it.".format(
                        self.name,
                        self._minimum_cpp_standard,
                        self.settings.compiler,
                        self.settings.compiler.version,
                    )
                )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        # prevent ROOT from overriding CMAKE_MODULE_PATH
        # tools.replace_in_file(
        #   f"{self._rootsrcdir}{os.sep}CMakeLists.txt",
        #   "set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)",
        #   "list(PREPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)",
        # )
        # ROOT builtin and CCI dependencies disagree on package name case
        # There is no way to override the dependency cmake_find_package name
        # see: https://github.com/conan-io/conan/issues/4430
        # So we must patch ROOT CMake to use the CCI package names
        for conanname, rootname, required in [  # ("lz4", "LZ4", True),
            # ("zstd", "ZSTD", True),
            # ("SQLite3", "Sqlite", False),
            # ("FFTW3", "FFTW", False),
        ]:
            rootuppername = rootname.upper()
            src = f"find_package({rootname})"
            if required:
                src = f"find_package({rootname} REQUIRED)"
            tools.replace_in_file(
                f"{self._rootsrcdir}/cmake/modules/SearchInstalledSoftware.cmake",
                src,
                f"""find_package({conanname} REQUIRED)
                set({rootuppername}_VERSION ${{{conanname}_VERSION}})
                set({rootuppername}_FOUND ${{{conanname}_FOUND}})
                set({rootuppername}_LIBRARIES ${{{conanname}_LIBRARIES}})
                add_library({rootname}::{rootname} INTERFACE IMPORTED)
                target_link_libraries ({rootname}::{rootname} INTERFACE {conanname}::{conanname})
                """,
            )

        os.remove(f"{self._rootsrcdir}/cmake/modules/FindTBB.cmake")

        # # Patch ROOT CMake to use Conan SQLITE
        tools.replace_in_file(
            f"{self._rootsrcdir}{os.sep}CMakeLists.txt",
            "project(ROOT)",
            """project(ROOT)
            # find_package(TBB REQUIRED)
            # set(TBB_LIBRARY TBB::tbb)
            # set(TBB_INCLUDE_DIR ${TBB_INCLUDE_DIRS})
            # #find_package(SQLite3 REQUIRED)
            # #set(SQLITE_INCLUDE_DIR ${SQLITE3_INCLUDE_DIRS})
            # #set(SQLITE_LIBRARIES SQLite::SQLite)
            find_package(OpenSSL REQUIRED)
            set(OPENSSL_VERSION ${OpenSSL_VERSION})
            # find_package(PNG REQUIRED)
            # set(PNG_PNG_INCLUDE_DIR ${PNG_INCLUDE_DIR})
            # find_package(LibLZMA REQUIRED)
            # set(LZMA_INCLUDE_DIR ${LibLZMA_INCLUDE_DIRS})
            # set(LZMA_LIBRARY LibLZMA::LibLZMA)
            # find_package(zstd REQUIRED)
            # set(ZSTD_LIBRARIES zstd::zstd)
            """,
        )
        # tools.replace_in_file(
        #     f"{self._rootsrcdir}{os.sep}cmake/modules/SearchInstalledSoftware.cmake",
        #     "include(FindPackageHandleStandardArgs)",
        #     """include(FindPackageHandleStandardArgs)
        #     include(${PROJECT_BINARY_DIR}/conan_paths.cmake)
        #     find_package(TBB REQUIRED)
        #     set(TBB_INCLUDE_DIR ${TBB_INCLUDE_DIRS})
        #     set(TBB_LIBRARY TBB::tbb)
        #     """
        # )
        # # ROOT defines its own find_package macro that interferes with finding Conan packages
        # # we need to disable this
        # tools.replace_in_file(f"{self._rootsrcdir}{os.sep}cmake/modules/SearchInstalledSoftware.cmake",
        #    "macro(find_package)",
        #    "macro(find_package_disabled)"
        # )
        # tools.replace_in_file(
        #     f"{self._rootsrcdir}{os.sep}cmake/modules/RootMacros.cmake",
        # )
        # Fix execute permissions on scripts
        scripts = [
            filename
            for pattern in (
                f"**{os.sep}configure",
                f"**{os.sep}*.sh",
                f"**{os.sep}*.csh",
                f"**{os.sep}*.bat",
            )
            for filename in glob(pattern, recursive=True)
        ]
        for s in scripts:
            self._make_file_executable(s)

    def _make_file_executable(self, filename):
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)

    @contextmanager
    def _configure_cmake(self) -> CMake:
        import shutil

        print(dir(self))
        print(os.getcwd())
        for f in ["opengl_system", "GLEW", "glu", "TBB", "LibXml2"]:
            shutil.copy(
                f"Find{f}.cmake",
                f"{self.source_folder}/{self._rootsrcdir}{os.sep}cmake/modules/",
            )
        self.deps_cpp_info["lz4"].names["cmake_find_package"] = "LZ4"
        if self._cmake is None:
            self._cmake = CMake(self)
            version = self.version.replace("v", "")
            cmakelibpath = ";".join(self.deps_cpp_info.lib_paths)
            cmakeincludepath = ";".join(self.deps_cpp_info.include_paths)
            self._cmake.configure(
                source_folder=f"root-{version}",
                defs={
                    # "CMAKE_TOOLCHAIN_FILE" : "conan_paths.cmake",
                    # TODO: Remove BUILD_SHARED_LIBS option when hooks issue is resolved
                    # (see: https://github.com/conan-io/hooks/issues/252)
                    "BUILD_SHARED_LIBS": "ON",
                    "fail-on-missing": "ON",
                    "CMAKE_CXX_STANDARD": self._CMAKE_CXX_STANDARD,
                    # Prefer builtins where available
                    "builtin_pcre": "OFF",
                    "builtin_lzma": "OFF",
                    "builtin_zstd": "OFF",
                    "builtin_xxhash": "ON",
                    "builtin_lz4": "OFF",
                    "builtin_afterimage": "ON",
                    "builtin_gsl": "ON",
                    "builtin_glew": "OFF",
                    "builtin_gl2ps": "ON",
                    "builtin_openssl": "OFF",
                    "builtin_fftw3": "OFF",
                    "builtin_cfitsio": "OFF",
                    "builtin_ftgl": "ON",
                    "builtin_davix": "OFF",
                    "builtin_tbb": "OFF",
                    "builtin_vdt": "ON",
                    # xrootd doesn't build with builtin openssl.
                    "builtin_xrootd": "OFF",
                    "xrootd": "OFF",
                    # No Conan packages available for these dependencies yet
                    "davix": "OFF",
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
                    "CMAKE_LIBRARY_PATH": cmakelibpath,
                    "CMAKE_INCLUDE_PATH": cmakeincludepath,
                    # Configure install directories
                    # Conan CCI hooks restrict the allowed install directory
                    # names but ROOT is very picky about where build/runtime
                    # resources get installed.
                    # Set install prefix to work around these limitations
                    # Following: https://github.com/conan-io/conan/issues/3695
                    "CMAKE_INSTALL_PREFIX": f"{self.package_folder}{os.sep}res",
                    "CMAKE_VERBOSE_MAKEFILE": "ON",
                    # "TBB_ROOT_DIR": self.deps_cpp_info.include_paths[0] + "/../"
                    # "OPENSSL_VERSION": self.deps_cpp_info["openssl"].version,
                    "PNG_PNG_INCLUDE_DIR": ";".join(
                        self.deps_cpp_info["libpng"].include_paths
                    ),
                    # "LZMA" : "LibLZMA::LibLZMA",
                    "LIBLZMA_INCLUDE_DIR": ";".join(
                        self.deps_cpp_info["xz_utils"].include_paths
                    ),
                },
            )
        yield self._cmake

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
        with self._configure_cmake() as cmake:
            cmake.install()
        self.copy("LICENSE.txt", dst="licenses")
        for dir in ["include", "lib", "bin"]:
            os.symlink(
                f"{self.package_folder}{os.sep}res{os.sep}{dir}",
                f"{self.package_folder}{os.sep}{dir}",
            )
        # Fix for CMAKE-MODULES-CONFIG-FILES (KB-H016)
        for cmakefile in glob(
            f"{self.package_folder}{os.sep}res{os.sep}cmake{os.sep}*Config*.cmake"
        ):
            os.remove(cmakefile)
        # Fix for CMAKE FILE NOT IN BUILD FOLDERS (KB-H019)
        os.remove(
            f"{self.package_folder}{os.sep}res{os.sep}tutorials{os.sep}CTestCustom.cmake"
        )

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "ROOT"
        self.cpp_info.names["cmake_find_package_multi"] = "ROOT"
        self.cpp_info.names["cmake_find_package"] = "ROOT"
        self.cpp_info.names["cmake_find_package_multi"] = "ROOT"
        # see root-config --libs for a list of libs
        self.cpp_info.libs = [
            "Core",
            "Imt",
            "RIO",
            "Net",
            "Hist",
            "Graf",
            "Graf3d",
            "Gpad",
            "ROOTVecOps",
            "Tree ",
            "TreePlayer",
            "Rint",
            "Postscript",
            "Matrix",
            "Physics",
            "MathCore",
            "Thread",
            "MultiProc",
            "ROOTDataFrame",
        ]
        self.cpp_info.builddirs = [f"res{os.sep}cmake"]
        self.cpp_info.build_modules.extend(
            [
                f"res{os.sep}cmake{os.sep}RootMacros.cmake",
                # f"res{os.sep}cmake{os.sep}ROOTUseFile.cmake",
            ]
        )
        self.cpp_info.resdirs = ["res"]

    def _fix_tbb_libs(self, libs: List[str]) -> List[str]:
        # Special treatment for tbb
        # (to handle issue https://github.com/conan-io/conan/issues/5428)
        return [(("lib" + name + ".so.2") if "tbb" in name else name) for name in libs]
