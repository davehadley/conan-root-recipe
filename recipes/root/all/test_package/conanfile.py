import os

from conans import CMake, ConanFile, RunEnvironment, tools


class RootTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake_find_package")
    requires = ("catch2/2.13.3",)

    def build(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("which rootcling")
            self.run("echo ROOTSYS is $ROOTSYS")
            self.run("pwd")
            print(f"DEBUG {env_build.vars}")
            self.run("echo ${LD_LIBRARY_PATH}")
            cmake = CMake(self)
            cmake.configure(defs={"CMAKE_VERBOSE_MAKEFILE": "ON"})
            cmake.build()

    def test(self):
        if not tools.cross_building(self):
            # self.run("ctest .", run_environment=True)
            self.run(".%sexample" % os.sep, run_environment=True)
