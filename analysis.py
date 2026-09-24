"""Reproducible command-line summary for the supermarket sales CSV."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent / "data" / "supermarket_sales.csv"
df = pd.read_csv(DATA)
df["Sales"] = pd.to_numeric(df["Quantity"], errors="coerce") * pd.to_numeric(df["Unit price"], errors="coerce")
df = df.dropna(subset=["Sales"])
print(f"Transactions: {len(df):,}")
print(f"Total sales: ₹{df['Sales'].sum():,.2f}")
print(f"Average transaction sales: ₹{df['Sales'].mean():,.2f}")
print(f"Average rating: {pd.to_numeric(df['Rating'], errors='coerce').mean():.2f}/5")
for dimension in ["Product", "Branch", "Payment", "Customer type"]:
    grouped = df.groupby(dimension).agg(sales=("Sales", "sum"), transactions=("Sales", "size")).sort_values("sales", ascending=False)
    print(f"\n{dimension} performance:\n{grouped.to_string(float_format=lambda x: f'${x:,.2f}')}")


