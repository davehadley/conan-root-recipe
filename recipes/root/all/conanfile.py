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
    generators = "cmake"
    requires = (
        "lz4/1.9.2",
        "opengl/system",
        "libxml2/2.9.10",
        "glu/system",
        "xorg/system",
        "openssl/1.1.1h",
        "libjpeg/9d",
        "libpng/1.6.37",
    )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

    def build(self):
        cmake = CMake(self)
        version = self.version.replace("v", "")
        cmake.configure(source_folder=f"root-{version}")
        cmake.build()
        cmake.test()

    def package(self):
        self.copy("*.h*", dst="include", src="include", keep_path=True)
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*", dst="bin", src="bin", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)

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
