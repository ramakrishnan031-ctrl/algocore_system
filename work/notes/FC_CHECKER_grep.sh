#!/bin/bash
# FC checker: read-only git grep at the baseline with the four mandatory exclusions.
# Usage: bash FC_CHECKER_grep.sh <git-grep options and pattern...> -- <pathspecs...>
# Writes nothing; runs no legacy code.
cd /home/claude/repos/legacy || exit 1
args=()
paths=()
seen=0
for a in "$@"; do
  if [ "$a" = "--" ]; then seen=1; continue; fi
  if [ $seen -eq 0 ]; then args+=("$a"); else paths+=("$a"); fi
done
[ ${#paths[@]} -eq 0 ] && paths=(.)
git grep "${args[@]}" 970aabf -- "${paths[@]}" \
  ':(exclude)config/accounts.csv' ':(exclude,glob)**/.env*' \
  ':(exclude,glob)**/*.local.yaml' ':(exclude,glob)**/*token*.json' | sed 's/^970aabf://'
