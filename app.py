"""Interactive supermarket sales analysis dashboard."""

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "supermarket_sales.csv"
REQUIRED = {"Product", "Branch", "City", "Customer type", "Quantity", "Unit price", "Payment", "Rating"}

st.set_page_config(page_title="Supermarket Sales | Analytics", page_icon="🛒", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1450px}
[data-testid="stMetric"] {background:#101a2c;border:1px solid #263650;padding:16px;border-radius:12px}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    df["Sales"] = pd.to_numeric(df["Quantity"], errors="coerce") * pd.to_numeric(df["Unit price"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    return df.dropna(subset=["Sales", "Quantity"])

st.title("🛒 Supermarket Sales Analysis")
st.caption("Explore product, branch, customer, and payment performance. Upload your internship dataset or explore the included demo data.")
uploaded = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])
source = uploaded if uploaded is not None else DATA_PATH
try:
    df = load_data(source)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

st.sidebar.header("Filters")
branches = st.sidebar.multiselect("Branch", sorted(df["Branch"].dropna().unique()), default=sorted(df["Branch"].dropna().unique()))
products = st.sidebar.multiselect("Product", sorted(df["Product"].dropna().unique()), default=sorted(df["Product"].dropna().unique()))
customers = st.sidebar.multiselect("Customer type", sorted(df["Customer type"].dropna().unique()), default=sorted(df["Customer type"].dropna().unique()))
filtered = df[df["Branch"].isin(branches) & df["Product"].isin(products) & df["Customer type"].isin(customers)]

if uploaded is None:
    st.info("Demo dataset: generated example transactions for demonstrating the workflow. Replace it with the assignment dataset before submitting findings.")
if filtered.empty:
    st.warning("No transactions match these filters.")
    st.stop()

total = filtered["Sales"].sum()
transactions = len(filtered)
top_product = filtered.groupby("Product")["Sales"].sum().idxmax()
top_branch = filtered.groupby("Branch")["Sales"].sum().idxmax()
avg_rating = filtered["Rating"].mean()
average_basket = total / transactions

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total sales", f"₹{total:,.2f}")
c2.metric("Transactions", f"{transactions:,}")
c3.metric("Average basket", f"₹{average_basket:,.2f}")
c4.metric("Top product", top_product)
c5.metric("Average rating", f"{avg_rating:.2f}/5" if pd.notna(avg_rating) else "N/A")

left,right = st.columns(2)
with left:
    by_product = filtered.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    st.subheader("Sales by product")
    st.plotly_chart(px.bar(by_product, x="Sales", y="Product", orientation="h", color="Sales", color_continuous_scale="teal", labels={"Sales":"Sales (₹)"}), use_container_width=True)
with right:
    by_branch = filtered.groupby("Branch", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    st.subheader("Sales by branch")
    st.plotly_chart(px.bar(by_branch, x="Branch", y="Sales", color="Branch", labels={"Sales":"Sales (₹)"}), use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Payment mix")
    pay = filtered["Payment"].value_counts().rename_axis("Payment").reset_index(name="Transactions")
    st.plotly_chart(px.pie(pay, names="Payment", values="Transactions", hole=.48), use_container_width=True)
with right:
    st.subheader("Customer type")
    cust = filtered.groupby("Customer type", as_index=False).agg(Sales=("Sales","sum"), Transactions=("Sales","size"))
    st.plotly_chart(px.bar(cust, x="Customer type", y="Sales", color="Customer type", labels={"Sales":"Sales (₹)"}), use_container_width=True)
    avg_by_customer = filtered.groupby("Customer type")["Sales"].mean()
    st.caption("Average transaction: " + " · ".join(f"{key}: ₹{value:,.2f}" for key, value in avg_by_customer.items()))

st.subheader("Branch × product performance")
pivot = filtered.pivot_table(index="Branch", columns="Product", values="Sales", aggfunc="sum", fill_value=0)
st.plotly_chart(px.imshow(pivot, text_auto=".0f", aspect="auto", color_continuous_scale="Tealgrn", labels={"color":"Sales (₹)"}), use_container_width=True)

with st.expander("View filtered transactions"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered data", filtered.to_csv(index=False), "filtered_supermarket_sales.csv", "text/csv")
st.caption(f"Top-performing branch in current filters: **{top_branch}** · Sales are calculated as Quantity × Unit price. This simplified assignment metric excludes tax and discounts.")




