mkdir root-build
cd root-build && conan install ../root 2>&1 && cmake -Dxrootd=OFF ../root && cmake --build . --parallel 4


