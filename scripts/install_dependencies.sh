#!/bin/bash

sudo python3 -m pip install pipenv
pipenv lock -r > requirements.txt
sudo python3 -m pip install -r requirements.txt