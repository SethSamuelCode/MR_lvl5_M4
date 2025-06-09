#!/bin/bash
frontend=git.sethsamuel.online/fluffy/mr_lvl5_m4_front
backend=git.sethsamuel.online/fluffy/mr_lvl5_m4_back

docker build . -f front.dockerfile -t $frontend
docker build . -f back.dockerfile -t $backend

docker push $frontend
docker push $backend

