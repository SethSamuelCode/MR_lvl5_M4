#!/bin/bash
frontend=git.sethsamuel.online/fluffy/mr_lvl5_m4_front_k8s
backend=git.sethsamuel.online/fluffy/mr_lvl5_m4_back

docker build . -f front.k8s.dockerfile -t $frontend
docker build . -f back.dockerfile -t $backend

docker push $frontend
docker push $backend

