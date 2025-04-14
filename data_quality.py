import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///data/paypal_credit.db"
engine = create_engine(DATABASE_URL)

def check_nulls(df, table_name):
    nulls = df.isnull().sum()
    if nulls.sum() > 0:
        print(f"❌ Nulls found in {table_name}:\n{nulls}")
    else:
        print(f"✅ No nulls in {table_name}")

def check_duplicates(df, table_name, key_column):
    duplicates = df.duplicated(subset=[key_column]).sum()
    if duplicates > 0:
        print(f"❌ Duplicates found in {table_name}: {duplicates}")
    else:
        print(f"✅ No duplicates in {table_name}")

def run_quality_checks():
    customers = pd.read_sql('SELECT * FROM customers_clean', engine)
    transactions = pd.read_sql('SELECT * FROM transactions_clean', engine)

    check_nulls(customers, "customers_clean")
    check_nulls(transactions, "transactions_clean")

    check_duplicates(customers, "customers_clean", "customer_id")
    check_duplicates(transactions, "transactions_clean", "transaction_id")

if __name__ == "__main__":
    run_quality_checks()
