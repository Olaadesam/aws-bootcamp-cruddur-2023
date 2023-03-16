#!/bin/bash

docker build -t frontend-react-js -f Dockerfile .

docker run -p 3000:3000 -d frontend-react-js


