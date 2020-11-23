import os

from conans import CMake, ConanFile, tools


class RootTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake_find_package")
    requires = ("catch2/2.13.3",)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            self.run("env", run_environment=True)
            self.run(".%sexample_targets" % os.sep, run_environment=True)
            self.run(".%sexample_vars" % os.sep, run_environment=True)
