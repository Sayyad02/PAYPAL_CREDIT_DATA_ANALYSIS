import pandas as pd
from faker import Faker
import random
import os

fake = Faker()
os.makedirs('data', exist_ok=True)

def generate_customers(n=100):
    customers = []
    for _ in range(n):
        customers.append({
            "customer_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "created_at": fake.date_this_decade()
        })
    return pd.DataFrame(customers)

def generate_transactions(customers, n=500):
    transactions = []
    for _ in range(n):
        customer = customers.sample(1).iloc[0]
        transactions.append({
            "transaction_id": fake.uuid4(),
            "customer_id": customer["customer_id"],
            "amount": round(random.uniform(10, 5000), 2),
            "currency": "USD",
            "timestamp": fake.date_time_this_year(),
            "status": random.choice(["COMPLETED", "FAILED", "PENDING"])
        })
    return pd.DataFrame(transactions)

def main():
    customers = generate_customers()
    transactions = generate_transactions(customers)

    customers.to_csv('data/customers.csv', index=False)
    transactions.to_csv('data/transactions.csv', index=False)
    print("✅ Fake data generated!")

if __name__ == "__main__":
    main()
