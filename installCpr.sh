git clone https://github.com/libcpr/cpr.git --depth 1
cd cpr && mkdir build && cd build
cmake .. -DCPR_USE_SYSTEM_CURL=ON -DBUILD_SHARED_LIBS=OFF 
cmake --build . --parallel
sudo cmake --install .