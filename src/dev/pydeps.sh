#!/bin/zsh
# Path: /usr/local/bin/pydeps.sh
# Description: Run pydeps to generate a dependency graph of a python project

# Usage: pydeps.sh <path to python project>

# Check if pydeps is installed
if ! command -v pydeps &> /dev/null
then
    echo "pydeps could not be found"
    exit
fi

python3 -m pydeps ~/Documents/University/Year\ 3/CE301\ -\ Capstone\ Project/Conquerors-of-Catan/src -T png -o ~/Documents/University/Year\ 3/CE301\ -\ Capstone\ Project/Conquerors-of-Catan/src/dev/dependencies.png --rmprefix src. --rankdir LR --cluster -x termcolor.termcolor
