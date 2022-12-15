import os
from enum import Enum

EMOTIONS = ["anger", "disgust", "joy", "fear", "neutral", "sadness", "surprise"]

CLIENT_URL = (
    "ling506-project.vercel.app"
    if os.environ.get("DEBUG", "False") == "False"
    else "http://localhost:3000"
)
