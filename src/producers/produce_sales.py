# src/producer/produce_sales.py

import time
import random
import json
import uuid
from datetime import datetime, timezone
from faker import Faker

fake = Faker()

PRODUCTS = [
    {"product_id": "P001", "product_name": "Widget A", "category": "Widgets"},
    {"product_id": "P002", "product_name": "Widget B", "category": "Widgets"},
    {"product_id": "P010", "product_name": "Gadget X", "category": "Gadgets"},
]


def gen_event():
    p = random.choice(PRODUCTS)
    event = {
        # timezone-aware UTC timestamp (no deprecation warning)
        "event_time": datetime.now(timezone.utc).isoformat(),
        "order_id": str(uuid.uuid4()),
        "customer_id": f"C{random.randint(1000, 1999)}",
        "product_id": p["product_id"],
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(10, 200), 2),
        "event_type": "order",
        "raw_payload": {},
    }
    return event


if __name__ == "__main__":
    while True:
        event = gen_event()
        print(json.dumps(event))
        time.sleep(random.uniform(0.2, 1.5))
