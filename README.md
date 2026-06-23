# 🔍 PriceWatch — Amazon Fake Discount Detector

Are Amazon's "sale" discounts real, or is the MRP inflated just to make the discount look bigger?

This project tracks real Amazon product prices over time and scores each one for **discount fraud** — flagging products where the claimed discount is likely the result of an inflated "original price" rather than a genuine price drop.

## 🚨 Key Finding

**8 of 17 products (47%) were flagged as suspicious** — claiming a discount greater than 50% off an MRP that doesn't hold up against the price actually charged.

## How it works

1. **Scrape** (`scraper.py`) — Tracks 17 products across 4 categories (Electronics, Kitchen, Beauty, Books) on Amazon.in daily, using ScraperAPI + BeautifulSoup to pull current price and MRP.
2. **Analyze** (`analysis.py`) — Cleans the data and computes:
   - **MRP volatility** — does the listed MRP change over time? (a red flag on its own)
   - **Price volatility** — how much does the actual selling price swing?
   - **Claimed Max Discount %** — compares the *highest* MRP ever shown against the *lowest* price ever charged. Anything above 50% is flagged suspicious.
3. **Visualize** (`dashboard.py`) — An interactive Streamlit dashboard with:
   - A "Wall of Shame" — top 5 worst offenders by Fraud Score
   - A Fraud Score gauge per product (`Claimed Discount % × 0.6 + MRP Inflation % × 0.4`)
   - Price history charts showing MRP vs. actual price over the tracking period
   - Category-level breakdown of who inflates the most
   - An MRP-vs-price scatter plot — products far below the "fair pricing" line are the most suspicious

## Data

- **17 products**, 4 categories, tracked daily over **4 days** (Apr 22–25, 2026)
- Source: Amazon.in, scraped via ScraperAPI

## Tech Stack

Python · BeautifulSoup · ScraperAPI · pandas · Streamlit · Plotly

## Run it yourself

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---
Built by [Muskan Varma](https://github.com/muskanvarmaa)
