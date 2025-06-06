#!/bin/bash

# Compile with C++17 standard
# Add multiple include paths
# Add verbose output flags
g++ -std=c++17 \
    -I /workspaces/MR_lvl5_M4/boost_1_85_0/libs/asio/include \
    -I /workspaces/MR_lvl5_M4/boostInstall/include \
    -I /workspaces/MR_lvl5_M4/libs \
    -I /usr/local/include/cpr \
    -I /usr/local/include/libcurl \
    -L /workspaces/MR_lvl5_M4/boostInstall/lib \
    -L /usr/local/lib \
    -DCROW_USE_BOOST \
    backend.cpp \
    -lpthread \
    -lboost_system \
    -lboost_regex \
    -lcpr \
    -lcurl \
    -lssl \
    -lcrypto \
    -lz \
    -lbrotlidec \
    -lbrotlicommon \
    -lzstd \
    -lidn2 \
    -lpsl \
    -lldap \
    -llber \
    -lnghttp2 \
    -lssh2 \
    -lrt \
    -lstdc++ \
    -lm \
    -o backend 2>&1 | tee build_log.txt