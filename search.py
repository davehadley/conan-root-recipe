#!/usr/bin/env python
from argparse import ArgumentParser
from subprocess import check_call

parser = ArgumentParser()
parser.add_argument("search", type=str)
args = parser.parse_args()

check_call(
    f'grep {args.search} $(find /tmp/tmpbuild/ -name "CMakeLists.txt" -or -name "*.cmake")',
    shell=True,
)
