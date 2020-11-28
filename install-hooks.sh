#!/usr/bin/env bash
pre-commit install
conan config install https://github.com/conan-io/hooks.git -sf hooks -tf hooks
conan config set hooks.conan-center
