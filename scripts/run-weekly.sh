#!/bin/sh
set -eu
export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:/opt/homebrew/bin:/usr/bin:/bin"
published=0

on_exit() {
  result=$1
  if [ "$result" -eq 0 ]; then
    message="Complete: the weekly paper checkpoint was pushed to GitHub."
    outcome=complete
  elif [ "$published" -eq 1 ]; then
    message="Partial: available papers were pushed; others need review. See the local log."
    outcome=partial
  else
    message="Failed: the weekly paper checkpoint was not fully published. See the local log."
    outcome=failed
  fi
  if /usr/bin/osascript -e 'on run argv' \
    -e 'display notification (item 1 of argv) with title "Weekly paper checkpoint"' \
    -e 'end run' "$message"; then
    printf 'Checkpoint notification sent: %s\n' "$outcome"
  else
    printf 'ERROR: Could not send checkpoint notification (%s)\n' "$outcome" >&2
    if [ "$result" -eq 0 ]; then
      result=1
    fi
  fi
  trap - 0
  exit "$result"
}

trap 'on_exit $?' 0
cd "$(dirname "$0")/.."

status=0
python3 scripts/checkpoint.py || status=$?
git add weeks papers
if ! git diff --cached --quiet; then
  git commit -m "Checkpoint weekly paper reading" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
fi
git push origin main
published=1
exit "$status"
