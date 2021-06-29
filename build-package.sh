#!/bin/bash
# build jello PIP package
# to install locally, run:   pip3 install jello-x.x.tar.gz

python3 setup.py sdist bdist_wheel
