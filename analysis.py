import pandas as pd
import numpy as np

# Load your data
df = pd.read_excel("price_tracker.xlsx")

# ── Step 1: Clean the data ──────────────────────────────

# Convert MRP and Current Price to numbers, errors become NaN
df["MRP"] = pd.to_numeric(df["MRP"], errors="coerce")
df["Current Price"] = pd.to_numeric(df["Current Price"], errors="coerce")

# Remove rows where price is missing
df = df.dropna(subset=["Current Price"])

# Remove Biotique — MRP is clearly wrong (₹1.38)
df = df[df["Product Name"] != "Biotique Honey Gel Face Cream"]

# Fix dates
df["Date"] = pd.to_datetime(df["Date"])

print("✅ Data cleaned!")
print(f"Total rows: {len(df)}")
print(f"Products: {df['Product Name'].nunique()}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

# ── Step 2: Find MRP volatility (price manipulation signal) ─

print("\n📊 MRP VOLATILITY PER PRODUCT (higher = more suspicious)")
mrp_stats = df.groupby("Product Name")["MRP"].agg(["min", "max", "nunique"])
mrp_stats.columns = ["Min MRP", "Max MRP", "Unique MRP Values"]
mrp_stats["MRP Change %"] = ((mrp_stats["Max MRP"] - mrp_stats["Min MRP"]) / mrp_stats["Min MRP"] * 100).round(1)
mrp_stats = mrp_stats.sort_values("MRP Change %", ascending=False)
print(mrp_stats)

# ── Step 3: Price volatility ────────────────────────────

print("\n📊 PRICE VOLATILITY PER PRODUCT")
price_stats = df.groupby("Product Name")["Current Price"].agg(["min", "max", "mean"])
price_stats.columns = ["Min Price", "Max Price", "Avg Price"]
price_stats["Price Swing %"] = ((price_stats["Max Price"] - price_stats["Min Price"]) / price_stats["Min Price"] * 100).round(1)
price_stats = price_stats.sort_values("Price Swing %", ascending=False)
print(price_stats)

# ── Step 4: Fake discount score ─────────────────────────

print("\n🚨 FAKE DISCOUNT ANALYSIS")

# For each product, use the HIGHEST MRP seen as the "inflated" MRP
# and compare against the LOWEST price seen
mrp_max = df.groupby("Product Name")["MRP"].max()
price_min = df.groupby("Product Name")["Current Price"].min()
price_avg = df.groupby("Product Name")["Current Price"].mean()

fake_df = pd.DataFrame({
    "Highest MRP Shown": mrp_max,
    "Lowest Price Seen": price_min,
    "Avg Price": price_avg.round(0)
}).dropna()

fake_df["Claimed Max Discount %"] = ((fake_df["Highest MRP Shown"] - fake_df["Lowest Price Seen"]) / fake_df["Highest MRP Shown"] * 100).round(1)
fake_df["Is Suspicious"] = fake_df["Claimed Max Discount %"] > 50

fake_df = fake_df.sort_values("Claimed Max Discount %", ascending=False)
print(fake_df)

# ── Step 5: Category summary ────────────────────────────

print("\n📦 CATEGORY SUMMARY")
cat_df = df.merge(fake_df[["Claimed Max Discount %"]], on="Product Name", how="left")
category_summary = cat_df.groupby("Category")["Claimed Max Discount %"].mean().round(1).sort_values(ascending=False)
print(category_summary)

print("\n✅ Analysis complete! Ready for dashboard.")