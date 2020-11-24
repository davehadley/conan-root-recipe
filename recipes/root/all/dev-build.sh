#!/usr/bin/env bash
# following: https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

export CONAN_HOOK_ERROR_LEVEL=40

conan source . --source-folder=/tmp/tmpbuild/source \
&& conan install . --install-folder=/tmp/tmpbuild/build \
&& conan build . --source-folder=/tmp/tmpbuild/source --build-folder=/tmp/tmpbuild/build \
&& conan package . --source-folder=/tmp/tmpbuild/source --build-folder=/tmp/tmpbuild/build --package-folder=/tmp/tmpbuild/package \
&& conan export-pkg -f .  testuser/testchannel --package-folder=/tmp/tmpbuild/package \
&& conan test test_package root/v6-22-02@testuser/testchannel 

