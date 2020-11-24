#!/usr/bin/env bash

export CONAN_HOOK_ERROR_LEVEL=40
# unset CONAN_HOOK_ERROR_LEVEL
conan create . root/v6-22-02@
