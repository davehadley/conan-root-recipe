# conan-root-recipe

A Conan recipe (https://conan.io/) for CERN ROOT data analysis framework (https://root.cern/).

# Development Instructions

After checkout run:
```
conda env create -f environment.yml
conda activate conan-root-recipe
pre-commit install
```

Yes that's right, we are using Anaconda to do our Conan package development. It's package managers all the way down.

From then on to setup the development environment do:

```
source setup.sh
```

To test the recipe do:
```
cd recipes/root/all && ./dev-build.sh
```
