#!/usr/bin/env python
# following: https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

import os
from subprocess import check_call

os.environ["CONAN_HOOK_ERROR_LEVEL"] = "40"
# try:
#    del os.environ["CONAN_HOOK_ERROR_LEVEL"]
# except Exception:
#    pass


def shell(cmd):
    return check_call(cmd, shell=True)


shell("conan source recipes/cern-root/all --source-folder=/tmp/tmpbuild/source")
shell("conan install recipes/cern-root/all --install-folder=/tmp/tmpbuild/build")
shell(
    "conan build recipes/cern-root/all --source-folder=/tmp/tmpbuild/source --build-folder=/tmp/tmpbuild/build"
)
shell(
    "conan package recipes/cern-root/all --source-folder=/tmp/tmpbuild/source --build-folder=/tmp/tmpbuild/build --package-folder=/tmp/tmpbuild/package"
)
shell(
    "conan export-pkg -f recipes/cern-root/all  testuser/testchannel --package-folder=/tmp/tmpbuild/package"
)
shell("conan test recipes/cern-root/all/test_package cern-root/v6-22-02@testuser/testchannel")
