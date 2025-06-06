#!/bin/bash
boostInstall=$(pwd)/boostInstall

export BOOST_ROOT=$boostInstall
export LD_LIBRARY_PATH=$boostInstall/lib:$LD_LIBRARY_PATH 
export CPLUS_INCLUDE_PATH=$boostInstall/include:$CPLUS_INCLUDE_PATH 