import pandas as pd


PERCENT_THRESHOLD = 15.0
GMV_THRESHOLD = 30000.0


def check_category_change(row):
    change_pct = row["change_pct"]
    change_amount = row["change_amount"]

    if pd.isna(change_pct):
        return False

    return (
        abs(change_pct) >= PERCENT_THRESHOLD
        and abs(change_amount) >= GMV_THRESHOLD
    )


def classify_change(row):
    if not check_category_change(row):
        return None

    if row["change_pct"] > 0:
        return "CATEGORY_GROWTH"

    return "CATEGORY_DECLINE"


def find_category_alerts(df):
    alerts = []

    for _, row in df.iterrows():

        if not check_category_change(row):
            continue

        alerts.append({
            "alert_type": classify_change(row),
            "category": row["category"],
            "month": row["month"],
            "current_gmv": float(row["current_gmv"]),
            "previous_gmv": float(row["previous_gmv"]),
            "change_pct": float(row["change_pct"]),
            "change_amount": float(row["change_amount"])
        })

    return alerts

def find_inactive_resellers(df):
    alerts = []

    for _, row in df.iterrows():
        if row["delivered_orders"] == 0:
            alerts.append({
                "alert_type": "RESELLER_INACTIVE",
                "reseller_id": row["reseller_id"],
                "reseller_name": row["reseller_name"],
                "region": row["region"],
                "city": row["city"],
                "delivered_orders": int(row["delivered_orders"]),
                "gmv": float(row["gmv"])
            })

    return alerts