#!/bin/bash

# Login to Instagram (Not recommended every time)
python3 login.py

# Start Flask server in background
python3 server.py &

# Start Telegram Bot
python3 bot.py
