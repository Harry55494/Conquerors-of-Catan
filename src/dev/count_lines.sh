#!/bin/zsh
# Path: /usr/local/bin/count_lines.sh
# Description: Counts line in /src directory

# Count lines in /src directory
echo "Counting lines in /src directory"
cd ..
# shellcheck disable=SC2038
find . -name '*.py' | xargs wc -l | sort -nr
