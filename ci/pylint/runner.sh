#!/bin/bash

# run pylint
pylint --load-plugins pylint_django $(ls -d */) | tee pylint.txt

# get badge
mkdir public
score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt)
anybadge --value=$score --file=public/pylint.svg pylint
echo "Pylint score was $score"

#cleanup
rm pylint.txt

exit 0
