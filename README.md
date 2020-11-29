# conan-root-recipe

A Conan recipe (https://conan.io/) for CERN ROOT data analysis framework (https://root.cern/).

# Development Instructions

After checkout run:
```
source setup-venv.sh && ./install-hooks.sh
```

To test the recipe do:
```
./dev-build.sh 1>log.out.txt 2>log.err.txt
```