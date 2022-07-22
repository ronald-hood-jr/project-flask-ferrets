#!/bin/sh
python3-virtualenv/bin/activate
python -m unittest discover -v tests
deactivate