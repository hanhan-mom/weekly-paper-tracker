#!/bin/sh
set -eu
export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:/opt/homebrew/bin:/usr/bin:/bin"
cd "$(dirname "$0")/.."

status=0
python3 scripts/checkpoint.py || status=$?
git add weeks papers
if ! git diff --cached --quiet; then
  git commit -m "Checkpoint weekly paper reading" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
fi
git push origin main
exit "$status"
