#!/bin/bash

# Check if session file exists before login
if [ ! -f "session-codexbots" ]; then
  echo "[!] Session not found, logging in..."
  python3 login.py
else
  echo "[✓] Session found, skipping login."
fi

# Start Flask server in background
python3 server.py &

# Start Telegram Bot
python3 bot.py
