import os
import instaloader

USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")

loader = instaloader.Instaloader()
loader.login(USERNAME, PASSWORD)
loader.save_session_to_file()
