import os

from conans import CMake, ConanFile, RunEnvironment, tools


class RootTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake_find_package")

    def build(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            cmake = CMake(self)
            cmake.configure(
                defs={"CMAKE_VERBOSE_MAKEFILE": "ON", "CMAKE_BUILD_TYPE": "Debug"}
            )
            cmake.build()

    def test(self):
        if not tools.cross_building(self):
            self.run(".{}testrootio".format(os.sep), run_environment=True)
