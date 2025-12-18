import psycopg2, json, sys
from time import sleep
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="salesdb",
    user="postgres",
    password="pavan1"
)

cur = conn.cursor()

def insert_raw(event):
    cur.execute("""
        INSERT INTO raw_sales_events (event_time, order_id, customer_id, product_id, store_id, quantity, price, currency, event_type, raw_payload)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        event["event_time"], event["order_id"], event.get("customer_id"),
        event.get("product_id"), event.get("store_id"), event.get("quantity"),
        event.get("price"), event.get("currency", "INR"), event.get("event_type"), json.dumps(event.get("raw_payload", {}))
    ))
    conn.commit()

parser.add_argument(
    "file",
    nargs="?",
    default="-",
    help="Path to JSONL file or '-' for stdin"
)

# Example: read from producer stdout or a file
with open("events.jsonl","r") as fh:
    for line in fh:
        event = json.loads(line)
        insert_raw(event)
        sleep(0.1)
