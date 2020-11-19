from pathlib import Path

from conans import CMake, ConanFile, tools


class RootConan(ConanFile):
    name = "root"
    version = "v6-22-02"
    license = "MIT"  # ROOT itself is LGPL-2.1-or-later
    author = "David Hadley <d.r.hadley@warwick.ac.uk>"
    url = "https://github.com/davehadley/conan-root-recipe"  # ROOT itself is located at: https://github.com/root-project/root
    description = "CERN ROOT data analysis framework."
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False]}
    # default_options = {"shared": False}
    generators = "txt"
    requires = (
        "opengl/system",
        "libxml2/2.9.10",
        "glu/system",
        "xorg/system",
        # "openssl/1.1.1h",
        # "libjpeg/9d",
        # "libpng/1.6.37",
        "sqlite3/3.33.0",
    )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], keep_permissions=True)

    def build(self):
        # Hack, fix configure scripts that have wrong permissions out of the zip file
        # for pattern in ["**/configure", "*.sh"]:
        #    for f in Path("./").glob(pattern):
        #        print(f"-- Making file executable {f}")
        #        os.chmod(f,  os.stat(f).st_mode | stat.S_IEXEC)
        # Paths and libraries, all
        print("-------- ALL --------------")
        print(self.deps_cpp_info.include_paths)
        print(self.deps_cpp_info.lib_paths)
        print(self.deps_cpp_info.bin_paths)
        print(self.deps_cpp_info.libs)
        print(self.deps_cpp_info.defines)
        print(self.deps_cpp_info.cflags)
        print(self.deps_cpp_info.cxxflags)
        print(self.deps_cpp_info.sharedlinkflags)
        print(self.deps_cpp_info.exelinkflags)
        print("DONE!")
        cmake = CMake(self)
        version = self.version.replace("v", "")
        cmake.configure(
            source_folder=f"root-{version}",
            defs={
                "fail-on-missing": "ON",
                "CMAKE_CXX_STANDARD": str(11),
                # prefer builtins where available
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
                # "builtin_asimage" : "OFF",
                # Doesn't build with builtin openssl.
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
                # set paths to Conan provided depedencies
                "LIBXML2_LIBRARY": self._getlibsopt("libxml2"),
                "LIBXML2_INCLUDE_DIR": self._getincludeopt("libxml2"),
                # "CMAKE_LIBRARY_PATH" : ";".join(self.deps_cpp_info.libs),
                # "CMAKE_INCLUDE_PATH" : ",".join(self.deps_cpp_info.include_paths),
                "SQLITE_INCLUDE_DIR": self._getincludeopt("sqlite3"),
                "SQLITE_LIBRARIES": self._getlibsopt("sqlite3"),
            },
        )
        cmake.build()
        cmake.install()
        cmake.test()

    # def package(self):
    #     self.copy("*.h*", dst="include", src="include", keep_path=True)
    #     self.copy("*.lib", dst="lib", src="lib", keep_path=False)
    #     self.copy("*", dst="bin", src="bin", keep_path=False)
    #     self.copy("*.so", dst="lib", src="lib", keep_path=False)
    #     self.copy("*.dylib", dst="lib", src="lib", keep_path=False)
    #     self.copy("*.a", dst="lib", src="lib", keep_path=False)

    def _getincludeopt(self, depname: str) -> str:
        return ";".join(self.deps_cpp_info[depname].include_paths)

    def _getlibsopt(self, depname: str) -> str:
        paths = self.deps_cpp_info[depname].lib_paths
        libpaths = [
            str(lib)
            for p in paths
            for pattern in ("*.so", "*.dll", "*.dylib", "*.lib", "*.a")
            for lib in Path(p).glob(pattern)
        ]
        assert len(libpaths) >= 1
        return ";".join(libpaths)

    def package_info(self):
        # get this list with root-config --libs
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
            "Tree",
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
