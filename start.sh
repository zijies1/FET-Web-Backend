#!/bin/bash
app="fet-api"
docker build -t ${app} .
docker run -d -p 56734:81 \
  --name=${app} \
  -v $PWD:/app ${app}
