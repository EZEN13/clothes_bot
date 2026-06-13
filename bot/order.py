import json
import time
from pathlib import Path

ORDERS_FILE = Path("data/orders.json")


def save_order(user_id: int, order: dict) -> None:
    orders = []
    if ORDERS_FILE.exists():
        try:
            orders = json.loads(ORDERS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            orders = []

    orders.append({
        "user_id": user_id,
        "timestamp": int(time.time()),
        **order
    })

    ORDERS_FILE.write_text(
        json.dumps(orders, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
