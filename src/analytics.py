import os
import sqlite3
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql")

DB_FILE = os.path.join(DATA_DIR, "meesho_reseller.db")


def run_query(sql_file):
    path = os.path.join(SQL_DIR, sql_file)

    with open(path, "r", encoding="utf-8") as f:
        query = f.read()

    conn = sqlite3.connect(DB_FILE)

    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


def get_category_metrics():
    return run_query("01_category_metrics.sql")


def get_reseller_activity():
    return run_query("02_reseller_activity.sql")


def get_region_metrics():
    return run_query("03_region_metrics.sql")


def get_category_mom():
    return run_query("04_category_mom.sql")