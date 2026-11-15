#!/bin/sh
# Keep the Mac awake and run Dadhichi rounds until the backlog is empty.
# Stop after the current round:  touch loop/STOP     Pause:  touch loop/PAUSE
cd "$(dirname "$0")/.." || exit 1
exec caffeinate -is python3 -I scripts/dadhichi_loop.py "$@"
