from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from uuid import UUID
import pandas as pd
import sqlite3

app = FastAPI()

# SQLAlchemy engine (optional use, helpful with pandas)
DATABASE_URL = "sqlite:///data/paypal_credit.db"
engine = create_engine(DATABASE_URL)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "PayPal Credit Data API"}

# Get a single customer by UUID
@app.get("/customer/{customer_id}")
def get_customer(customer_id: UUID):
    conn = sqlite3.connect("data/paypal_credit.db")
    conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers WHERE id = ?", (str(customer_id),))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"customer": dict(row)}

# Get all transactions
@app.get("/transactions/")
def get_transactions():
    try:
        df = pd.read_sql_query("SELECT * FROM transactions_clean", engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
