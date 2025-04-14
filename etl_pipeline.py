import pandas as pd
from sqlalchemy import create_engine
import hashlib

DATABASE_URL = "sqlite:///data/paypal_credit.db"
engine = create_engine(DATABASE_URL)

def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

def transform_data():
    customers = pd.read_sql('SELECT * FROM customers_staging', engine)
    transactions = pd.read_sql('SELECT * FROM transactions_staging', engine)

    customers['email'] = customers['email'].apply(hash_email)

    transactions['risk_flag'] = transactions['amount'].apply(lambda x: 'HIGH' if x > 3000 else 'NORMAL')

    customers.to_sql('customers_clean', engine, if_exists='replace', index=False)
    transactions.to_sql('transactions_clean', engine, if_exists='replace', index=False)

    print("✅ ETL pipeline completed!")

if __name__ == "__main__":
    transform_data()
