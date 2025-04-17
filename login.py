# login_or_load.py
import instaloader
import os

USERNAME = "codexbots"
PASSWORD = "aditya@2005"
SESSION_FILE = "session-codexbots"

loader = instaloader.Instaloader(save_metadata=False, download_comments=False, post_metadata_txt_pattern='')

if os.path.exists(SESSION_FILE):
    print("[✓] Logging in using session...")
    loader.load_session_from_file(USERNAME, SESSION_FILE)
else:
    print("[!] Logging in with credentials...")
    loader.login(USERNAME, PASSWORD)
    loader.save_session_to_file(SESSION_FILE)
    print("[✓] Session saved.")

# Export loader
INSTALOADER = loader
