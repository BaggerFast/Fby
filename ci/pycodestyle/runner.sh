#!/bin/bash

mkdir public
pycodestyle . --ignore=E501 --statistics > public/pycodestyle.txt

exit 0

