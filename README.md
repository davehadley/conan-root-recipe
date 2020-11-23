# conan-root-recipe

A Conan recipe (https://conan.io/) for CERN ROOT data analysis framework (https://root.cern/).

# Development Instructions

Setup environment with:
```
conda env create -f environment.yml
conda activate conan-root-recipe
pre-commit install
```

Yes that's right, we are using Anaconda to do our Conan package development. It's package managers all the way down.

To test the recipe do:
```
cd recipes/root/all && ./dev-build.sh
```
