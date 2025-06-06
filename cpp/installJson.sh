#!/bin/bash

# Install nlohmann/json
sudo apt-get update
sudo apt-get install -y nlohmann-json3-dev

# Alternative manual installation
# mkdir -p /tmp/json
# cd /tmp/json
# wget https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
# tar -xvf json.tar.xz
# cd json
# mkdir build && cd build
# cmake ..
# make
# sudo make install
