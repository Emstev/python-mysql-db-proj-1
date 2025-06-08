#!/bin/bash

# Exit on error
set -e

# Change ownership
sudo chown -R ubuntu:ubuntu ~/python-mysql-db-proj-1

# Move into the project directory
cd ~/python-mysql-db-proj-1

# Install venv module if needed
sudo apt-get update
sudo apt-get install -y python3.12-venv

# Create and activate virtual environment, install deps
python3 -m venv venv
source venv/bin/activate
pip install flask pymysql
