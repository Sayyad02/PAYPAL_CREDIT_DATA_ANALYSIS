import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = "sqlite:///data/paypal_credit.db"
engine = create_engine(DATABASE_URL)

def ingest_csv_to_db(file_path, table_name):
    df = pd.read_csv(file_path)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"✅ Ingested {table_name} into DB")

def main():
    os.makedirs('data', exist_ok=True)
    ingest_csv_to_db('data/customers.csv', 'customers_staging')
    ingest_csv_to_db('data/transactions.csv', 'transactions_staging')

if __name__ == "__main__":
    main()
