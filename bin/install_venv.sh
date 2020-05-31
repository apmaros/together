#!/bin/bash

# Installs virtual environment
#   - purges current environment to start from clear state

echo "installing dev environment"

echo "purging existing environment"
rm -rf ./venv
echo "initializing new environment"
virtualenv venv
source ./venv/bin/activate
echo "installing dependencies"
pip install -r requirements.txt

