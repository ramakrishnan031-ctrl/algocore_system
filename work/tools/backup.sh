#!/bin/bash
# A08 fieldwork backup. Fails closed on every check. Writes ONLY branch wip/a08-fieldwork of the approved
# algocore_system repository, from the separate backup clone, staging ONLY its work/ subtree; never main; no merge.
set -euo pipefail
B=/home/claude/a08_backup
SRC=/home/claude/a08
TOOLS=/home/claude/a08_tools
BRANCH=wip/a08-fieldwork
CONF=/home/claude/a08_backup.conf
REQ_DIRS="briefs parts check evidence out rtr treat notes status"
REQ_TOOLS="scan.py backup.sh"
NOTE="${1:-backup}"
fail() { echo "BACKUP REFUSED: $*"; exit 10; }
[ -f "$CONF" ] || fail "settings file missing"
declare -A C=()
while IFS= read -r line || [ -n "$line" ]; do
  [ -z "$line" ] && continue
  k=${line%%=*}; v=${line#*=}
  case "$k" in APPROVED|APPROVED_ALT|GIT_NAME|GIT_EMAIL|COAUTHOR) C[$k]=$v;; *) fail "unknown settings key";; esac
done < "$CONF"
for k in APPROVED APPROVED_ALT GIT_NAME GIT_EMAIL COAUTHOR; do [ -n "${C[$k]:-}" ] || fail "settings key $k missing"; done
APPROVED=${C[APPROVED]}; APPROVED_ALT=${C[APPROVED_ALT]}
case "$APPROVED" in https://github.com/*.git) ;; *) fail "settings APPROVED is not a github.com https .git URL";; esac
[ "$APPROVED_ALT" = "${APPROVED%.git}" ] || fail "settings APPROVED_ALT must equal APPROVED without .git"
exec 9>/home/claude/a08_backup.lock; flock -w 600 9 || fail "lock not obtained within 600 s"
[ -d "$SRC" ] && [ "$(cd "$SRC" && pwd -P)" = "$SRC" ] || fail "source $SRC missing or not the real path"
for d in $REQ_DIRS; do [ -d "$SRC/$d" ] || fail "required source folder $SRC/$d missing"; done
for t in $REQ_TOOLS; do [ -f "$TOOLS/$t" ] || fail "required tool $TOOLS/$t missing"; done
[ -d "$B" ] || fail "backup clone $B missing"
cd "$B"
[ "$(git rev-parse --show-toplevel)" = "$B" ] || fail "top-level is not $B"
[ "$(git rev-parse --abbrev-ref HEAD)" = "$BRANCH" ] || fail "backup clone is not on $BRANCH"
ok_url() { [ "$1" = "$APPROVED" ] || [ "$1" = "$APPROVED_ALT" ]; }
mapfile -t FURLS < <(git remote get-url --all origin)
mapfile -t PURLS < <(git remote get-url --push --all origin)
[ "${#FURLS[@]}" -eq 1 ] && ok_url "${FURLS[0]}" || fail "origin must have exactly one approved fetch URL"
[ "${#PURLS[@]}" -eq 1 ] && ok_url "${PURLS[0]}" || fail "origin must have exactly one approved push URL"
while read -r key val; do
  [ -z "${key:-}" ] && continue
  case "$APPROVED" in "$val"*) fail "URL rewrite $key=$val would change the approved address";; esac
done < <(git config --get-regexp '^url\..*\.(insteadof|pushinsteadof)$' || true)
OTHER=$(git status --porcelain --untracked-files=all | grep -v -E '^.. work/' || true)
[ -z "$OTHER" ] || fail "changes outside work/ in the backup clone"
rm -rf work; mkdir -p work/tools
for d in $REQ_DIRS; do cp -a "$SRC/$d" work/ || fail "copy of $d failed"; done
for f in "$TOOLS"/*.py "$TOOLS"/*.sh; do [ -f "$f" ] || continue; cp -a "$f" work/tools/ || fail "copy of $f failed"; done
for d in $REQ_DIRS; do diff -rq "$SRC/$d" "work/$d" >/dev/null || fail "copy of $d is not identical to the source"; done
for t in $REQ_TOOLS; do cmp -s "$TOOLS/$t" "work/tools/$t" || fail "copy of tool $t is not identical"; done
python3 -I "$TOOLS/scan.py" work || { echo "BACKUP BLOCKED: scan hits"; exit 2; }
git add -A -- work
BAD=$(git diff --cached --name-only | grep -v -E '^work/' || true)
[ -z "$BAD" ] || { git reset -q; fail "staged paths outside work/"; }
if ! git diff --cached --quiet; then
  printf 'wip(A08): fieldwork backup - %s - %s\n\n%s\n' "$NOTE" "$(TZ=Asia/Kolkata date '+%d-%b-%Y %H:%M IST')" "${C[COAUTHOR]}" > /tmp/a08_bk_msg.txt
  GIT_AUTHOR_NAME=${C[GIT_NAME]} GIT_AUTHOR_EMAIL=${C[GIT_EMAIL]} GIT_COMMITTER_NAME=${C[GIT_NAME]} GIT_COMMITTER_EMAIL=${C[GIT_EMAIL]} \
    git commit -q -F /tmp/a08_bk_msg.txt || { git reset -q; fail "commit failed or was rejected by a configured hook"; }
fi
OUT=$(git push "$APPROVED" "refs/heads/$BRANCH:refs/heads/$BRANCH" 2>&1) || { echo "$OUT"; fail "push failed or was rejected by a hook"; }
L=$(git rev-parse HEAD); R=$(git ls-remote "$APPROVED" "refs/heads/$BRANCH" | cut -f1)
[ -n "$R" ] && [ "$L" = "$R" ] && echo "BACKUP OK $L" || { echo "BACKUP REMOTE MISMATCH"; exit 3; }
