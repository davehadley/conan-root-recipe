mkdir root-build
cd root-build && conan install ../root 2>&1 && cmake ../root && cmake --build . 


