#!/bin/bash

docker build \
    -f docker/Dockerfile \
    -t stock-analysis-ai-agent:1.0 .
