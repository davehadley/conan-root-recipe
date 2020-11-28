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


shell("conan source recipes/root/all --source-folder=/tmp/tmpbuild/source")
shell("conan install recipes/root/all --install-folder=/tmp/tmpbuild/build")
shell(
    "conan build recipes/root/all --source-folder=/tmp/tmpbuild/source --build-folder=/tmp/tmpbuild/build"
)
shell(
    "conan package recipes/root/all --source-folder=/tmp/tmpbuild/source --build-folder=/tmp/tmpbuild/build --package-folder=/tmp/tmpbuild/package"
)
shell(
    "conan export-pkg -f recipes/root/all  testuser/testchannel --package-folder=/tmp/tmpbuild/package"
)
shell("conan test recipes/root/all/test_package root/v6-22-02@testuser/testchannel")
