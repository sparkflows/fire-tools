#!/bin/sh
#source "${APP_HOME}"/venv/bin/activate
#alias python=python3.8
python3.8 --version
python --version
pip list | grep notebook
jupyter notebook &
