#!/bin/bash

mkdir public
pycodestyle . --statistics > public/pycodestyle.txt

exit 0

