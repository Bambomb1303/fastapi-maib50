from pathlib import Path
import json

with open("music_data.json", "r", encoding="utf-8") as f:
    music_data = json.load(f)    

MUSIC_DATA = music_data
BASE_DIR = Path(__file__).resolve().parent.parent

version_map = {
    "2020": "maimai でらっくす",
    "2021": "maimai でらっくす Splash",
    "2022": "maimai でらっくす UNiVERSE",
    "2023": "maimai でらっくす FESTiVAL",
    "2024": "maimai でらっくす BUDDiES",
    "2025": "maimai でらっくす PRiSM"
}

