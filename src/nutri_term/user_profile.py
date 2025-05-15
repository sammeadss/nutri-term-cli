import json
from pathlib import Path
from typing import Dict, Optional

CONFIG_DIR = Path.home() / "nutri-term"
PROFILE_FILE = CONFIG_DIR / "profile.json"

def save_profile(data: Dict) -> None:
    CONFIG_DIR.mkdir(exist_ok=True)
    with PROFILE_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_profile() -> Optional[Dict]:
    if not PROFILE_FILE.exists():
        return None
    with PROFILE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)
   
