#!/bin/bash

# Clone git repository
git clone https://github.com/pradnyayeole/BookClub.git

# Change directory to cloned repository
cd BookClub

# Pull Docker image
sudo docker pull cloudcomputingproject:latest

# Run Docker container
sudo docker run -p 5000:5000 cloudcomputingproject:latest

