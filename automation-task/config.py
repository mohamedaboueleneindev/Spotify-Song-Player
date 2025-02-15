"""
Configuration for the Spotify bot.
"""

import logging

URL = "https://open.spotify.com/"

DEFAULT_WAIT_TIME = 10
DEFAULT_SLEEP_TIME = 1

SONG_NAME = "Hello Adele"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
