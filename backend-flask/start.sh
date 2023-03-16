#!/bin/bash

docker build -t backend-flask -f Dockerfile .

docker run -it backend-flask


