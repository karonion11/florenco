import json
from pathlib import Path

FILE = Path('subscribers.json')

def load_subscribers() -> list:
    if FILE.exists():
        with open(FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_subscribers(subs: list) -> None:
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(subs, f)

def toggle_subscription(user_id: int) -> bool:
    subs = load_subscribers()
    if user_id in subs:
        subs.remove(user_id)
        save_subscribers(subs)
        return False
    else:
        subs.append(user_id)
        save_subscribers(subs)
        return True
