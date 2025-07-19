import json
from pathlib import Path
from typing import Optional, Dict

FOOD_DB_PATH = Path(__file__).parent.parent.parent / "data" / "foods.json"


def load_food_database() -> Dict[str, Dict[str, float]]:
    with open(FOOD_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def lookup_food(food_name: str) -> Optional[Dict[str, float]]:
    db = load_food_database()
    return db.get(food_name.lower()) 