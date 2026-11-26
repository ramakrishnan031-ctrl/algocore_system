#!/usr/bin/env bash
# P04 writer helper: repository-wide git grep at the baseline with the four mandatory exclusions.
# Usage: bash P04_grep.sh [git-grep options...] -e PATTERN [-- extra pathspecs]
# Reads the legacy clone only (git grep on the commit object); writes nothing.
cd /home/claude/repos/legacy || exit 1
args=()
paths=()
seen_dd=0
for a in "$@"; do
  if [ "$a" = "--" ]; then seen_dd=1; continue; fi
  if [ $seen_dd -eq 1 ]; then paths+=("$a"); else args+=("$a"); fi
done
if [ ${#paths[@]} -eq 0 ]; then paths=("."); fi
git grep "${args[@]}" 970aabf -- "${paths[@]}" \
  ':(exclude)config/accounts.csv' ':(exclude,glob)**/.env*' \
  ':(exclude,glob)**/*.local.yaml' ':(exclude,glob)**/*token*.json'
