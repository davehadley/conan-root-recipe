#!/usr.bin/env bash
# following: https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

conan source . --source-folder=tmp/source \
&& conan install . --install-folder=tmp/build \
&& conan build . --source-folder=tmp/source --build-folder=tmp/build \
&& conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package \
&& conan export-pkg . user/channel --source-folder=tmp/source --build-folder=tmp/build \
&& conan test test_package root/v6-22-02@testuser/testchannel
