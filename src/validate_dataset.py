import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

resellers_file = os.path.join(DATA_DIR, "resellers.csv")
orders_file = os.path.join(DATA_DIR, "orders.csv")
db_file = os.path.join(DATA_DIR, "meesho_reseller.db")


resellers = pd.read_csv(resellers_file)
orders = pd.read_csv(orders_file)

print("Resellers:", len(resellers))
print("Orders:", len(orders))

print("\nReseller columns:")
print(list(resellers.columns))

print("\nOrder columns:")
print(list(orders.columns))


print("\nMissing values:")
print("Resellers:", resellers.isnull().sum().sum())
print("Orders:", orders.isnull().sum().sum())


print("\nDuplicate IDs:")
print("Reseller IDs:", resellers["reseller_id"].duplicated().sum())
print("Order IDs:", orders["order_id"].duplicated().sum())


print("\nRegions:")
print(resellers["region"].value_counts())

print("\nCategories:")
print(orders["category"].value_counts())

print("\nMonths:")
print(orders["month"].value_counts())

print("\nOrder statuses:")
print(orders["status"].value_counts())


print("\nChecking reseller references...")

valid_reseller_ids = set(resellers["reseller_id"])
order_reseller_ids = set(orders["reseller_id"])

missing_resellers = order_reseller_ids - valid_reseller_ids

print("Orders with invalid reseller IDs:", len(missing_resellers))


print("\nZero-order resellers:")

order_counts = orders["reseller_id"].value_counts()

resellers_with_no_orders = resellers[
    ~resellers["reseller_id"].isin(order_counts.index)
]

print(resellers_with_no_orders[
    ["reseller_id", "reseller_name", "region"]
])


print("\nChecking database...")

conn = sqlite3.connect(db_file)

reseller_count = conn.execute(
    "SELECT COUNT(*) FROM resellers"
).fetchone()[0]

order_count = conn.execute(
    "SELECT COUNT(*) FROM orders"
).fetchone()[0]

conn.close()

print("Database resellers:", reseller_count)
print("Database orders:", order_count)


print("\nValidation complete.")