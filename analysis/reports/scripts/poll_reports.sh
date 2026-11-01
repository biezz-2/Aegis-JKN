#!/bin/bash
DIR="N:/HEALTHKATHON/analysis/reports"
LOG="N:/HEALTHKATHON/analysis/reports/scripts/poll_log.txt"
LAST=""
IDLE=0
START=$(date +%s)
MAX=$((50*60))
IDLE_MAX=$((8*60))
while true; do
  CUR=$(ls -1 "$DIR"/*.md 2>/dev/null | sort | tr '\n' '|')
  NOW=$(date +%s)
  ELAPSED=$((NOW-START))
  if [ "$CUR" != "$LAST" ]; then
    echo "[$(date +%H:%M:%S)] CHANGE detected. Files: $(echo "$CUR" | tr '|' ' ')" >> "$LOG"
    LAST="$CUR"
    IDLE=0
  else
    IDLE=$((IDLE+60))
    echo "[$(date +%H:%M:%S)] no change. idle=${IDLE}s elapsed=${ELAPSED}s" >> "$LOG"
  fi
  if [ "$IDLE" -ge "$IDLE_MAX" ]; then
    echo "POLL_COMPLETE: idle 8 min reached at elapsed ${ELAPSED}s" >> "$LOG"
    echo "POLL_COMPLETE_IDLE"
    exit 0
  fi
  if [ "$ELAPSED" -ge "$MAX" ]; then
    echo "POLL_COMPLETE: 50 min max reached" >> "$LOG"
    echo "POLL_COMPLETE_MAX"
    exit 0
  fi
  sleep 60
done
