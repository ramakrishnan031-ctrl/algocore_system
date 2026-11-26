#!/bin/bash
# P06 writer: reader search for every SRDetectorConfig / StructureExitConfig field (read-only git grep at 970aabf)
cd /home/claude/repos/legacy
X=(':(exclude)config/accounts.csv' ':(exclude,glob)**/.env*' ':(exclude,glob)**/*.local.yaml' ':(exclude,glob)**/*token*.json')
for k in "$@"; do
  echo "### $k"
  git grep -n -w "$k" 970aabf -- '*.py' "${X[@]}" | grep -v -E '^970aabf:tests/' | sed 's/^970aabf://' | cut -c1-200
done
