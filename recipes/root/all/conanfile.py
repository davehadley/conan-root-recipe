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
        tools.get(**self.conan_data["sources"][self.version])

    def build(self):
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
                "builtin_xrootd": "ON",
                "builtin_ftgl": "ON",
                "builtin_davix": "ON",
                "builtin_tbb": "ON",
                "builtin_vdt": "ON",
                # "builtin_asimage" : "OFF",
                # No Conan packages available for these dependencies yet
                "pythia6": "OFF",
                "pythia8": "OFF",
                "mysql": "OFF",
                "oracle": "OFF",
                "pgsql": "OFF",
                "gfal": "OFF",
                "tmva-pymva": "OFF",
                # set paths to Conan provided depedencies
                "LIBXML2_LIBRARY": str(self.deps_cpp_info["libxml2"].lib_paths[0]),
                "LIBXML2_INCLUDE_DIR": str(
                    self.deps_cpp_info["libxml2"].include_paths[0]
                ),
                # "CMAKE_LIBRARY_PATH" : ";".join(self.deps_cpp_info.libs),
                # "CMAKE_INCLUDE_PATH" : ",".join(self.deps_cpp_info.include_paths),
                "SQLITE_INCLUDE_DIR": str(
                    self.deps_cpp_info["sqlite3"].include_paths[0]
                ),
                "SQLITE_LIBRARIES": str(self.deps_cpp_info["sqlite3"].lib_paths[0]),
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
