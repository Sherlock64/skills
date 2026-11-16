#!/bin/sh
# Print a git tree id for the working tree as it is now (tracked and untracked, minus ignored),
# without touching the real index. Same output means the same files.
set -e
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
cp "$(git rev-parse --git-path index)" "$tmp" 2>/dev/null || rm -f "$tmp"
GIT_INDEX_FILE=$tmp git add -A
GIT_INDEX_FILE=$tmp git write-tree
