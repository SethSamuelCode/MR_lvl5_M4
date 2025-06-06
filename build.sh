#!/bin/bash

# Compile with C++17 standard
# Statically link libraries
# Add multiple include paths
g++ -std=c++17 -static \
    -I /workspaces/MR_lvl5_M4/boost_1_85_0/libs/asio/include \
    -I /workspaces/MR_lvl5_M4/boostInstall/include \
    -I /workspaces/MR_lvl5_M4/libs \
    -L /workspaces/MR_lvl5_M4/boostInstall/lib \
    -DCROW_USE_BOOST \
    backend.cpp \
    -lpthread \
    -lboost_system \
    -lboost_regex \
    -lrt \
    -o backend