#!/bin/bash

# ==== CONFIG ====
PROFILE_NAME="chromium-4chan"
PROFILE_DIR="$HOME/snap/chromium/common/$PROFILE_NAME"
REMOTE_PORT=9222
# ================

mkdir -p "$PROFILE_DIR"

echo "🚀 Launching Snap Chromium with persistent profile at: $PROFILE_DIR"
chromium --remote-debugging-port=$REMOTE_PORT --user-data-dir="$PROFILE_DIR" &
