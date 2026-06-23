import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ── Page config ────────────────────────────────────────
st.set_page_config(
    page_title="Fake Discount Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0A0A0A; color: #F0F0F0; }
    
    /* Headline style */
    .headline {
        font-size: 48px;
        font-weight: 900;
        color: #FF2B2B;
        text-transform: uppercase;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .subheadline {
        font-size: 18px;
        color: #AAAAAA;
        margin-top: 8px;
        font-style: italic;
    }
    .breaking {
        background: #FF2B2B;
        color: white;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* KPI cards */
    .kpi-card {
        background: #1A1A1A;
        border: 1px solid #333;
        border-left: 4px solid #FF2B2B;
        border-radius: 4px;
        padding: 20px;
        text-align: center;
    }
    .kpi-value {
        font-size: 42px;
        font-weight: 900;
        color: #FF2B2B;
    }
    .kpi-label {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    
    /* Wall of shame card */
    .shame-card {
        background: #1A0000;
        border: 1px solid #FF2B2B;
        border-radius: 8px;
        padding: 20px;
        margin: 8px 0;
        position: relative;
    }
    .shame-rank {
        font-size: 48px;
        font-weight: 900;
        color: #FF2B2B;
        opacity: 0.3;
        position: absolute;
        top: 10px;
        right: 20px;
    }
    .shame-name {
        font-size: 20px;
        font-weight: 700;
        color: #FF6B6B;
    }
    .shame-score {
        font-size: 36px;
        font-weight: 900;
        color: #FF2B2B;
    }
    .shame-detail {
        font-size: 13px;
        color: #888;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 22px;
        font-weight: 800;
        color: #FF2B2B;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #FF2B2B;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }

    /* Divider */
    hr { border-color: #222; }

    /* Metric overrides */
    [data-testid="metric-container"] {
        background: #1A1A1A;
        border: 1px solid #333;
        border-left: 4px solid #FF2B2B;
        padding: 16px;
        border-radius: 4px;
    }
    [data-testid="metric-container"] label { color: #888 !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #FF2B2B !important; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# ── Load & clean data ──────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("price_tracker.xlsx")
    df["MRP"] = pd.to_numeric(df["MRP"], errors="coerce")
    df["Current Price"] = pd.to_numeric(df["Current Price"], errors="coerce")
    df = df.dropna(subset=["Current Price"])
    df = df[df["Product Name"] != "Biotique Honey Gel Face Cream"]
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ── Compute scores ─────────────────────────────────────
mrp_max = df.groupby("Product Name")["MRP"].max()
mrp_min = df.groupby("Product Name")["MRP"].min()
price_min = df.groupby("Product Name")["Current Price"].min()
price_avg = df.groupby("Product Name")["Current Price"].mean().round(0)
price_max = df.groupby("Product Name")["Current Price"].max()
category = df.groupby("Product Name")["Category"].first()

summary = pd.DataFrame({
    "Highest MRP Shown": mrp_max,
    "Lowest MRP Shown": mrp_min,
    "Lowest Price Seen": price_min,
    "Highest Price Seen": price_max,
    "Avg Price": price_avg,
    "Category": category
}).dropna().reset_index()

summary["Claimed Discount %"] = ((summary["Highest MRP Shown"] - summary["Lowest Price Seen"]) / summary["Highest MRP Shown"] * 100).round(1)
summary["MRP Inflation %"] = ((summary["Highest MRP Shown"] - summary["Lowest MRP Shown"]) / summary["Lowest MRP Shown"] * 100).round(1)
summary["Fraud Score"] = (summary["Claimed Discount %"] * 0.6 + summary["MRP Inflation %"].clip(0, 100) * 0.4).round(1)
summary["Is Suspicious"] = summary["Claimed Discount %"] > 50
summary = summary.sort_values("Fraud Score", ascending=False).reset_index(drop=True)

# ── HEADER ─────────────────────────────────────────────
st.markdown('<div class="breaking">⚠ EXCLUSIVE INVESTIGATION</div>', unsafe_allow_html=True)
st.markdown('<div class="headline">Are Amazon\'s<br>Discounts Real?</div>', unsafe_allow_html=True)
st.markdown('<div class="subheadline">I tracked 17 products for 4 days. What I found will make you think twice before your next sale purchase.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI CARDS ──────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Products Investigated", len(summary))
with c2:
    n = summary["Is Suspicious"].sum()
    st.metric("Caught Inflating MRP", f"{n} of {len(summary)}", delta=f"{round(n/len(summary)*100)}% suspicious", delta_color="inverse")
with c3:
    st.metric("Highest Fraud Score", f"{summary['Fraud Score'].max()}/100", delta=summary.iloc[0]["Product Name"], delta_color="inverse")
with c4:
    st.metric("Most Honest Category", "Beauty", delta="Only 5.2% avg discount claimed")

st.markdown("---")

# ── WALL OF SHAME ──────────────────────────────────────
st.markdown('<div class="section-header">🏆 Wall of Shame — Top 5 Worst Offenders</div>', unsafe_allow_html=True)

top5 = summary.head(5)
cols = st.columns(5)
for i, (_, row) in enumerate(top5.iterrows()):
    with cols[i]:
        st.markdown(f"""
        <div class="shame-card">
            <div class="shame-rank">#{i+1}</div>
            <div class="shame-name">{row['Product Name'].split()[0]} {row['Product Name'].split()[1] if len(row['Product Name'].split()) > 1 else ''}</div>
            <div class="shame-score">{row['Fraud Score']}</div>
            <div class="shame-detail">Fraud Score</div>
            <div class="shame-detail" style="margin-top:8px">Claimed: <b style="color:#FF6B6B">{row['Claimed Discount %']}% off</b></div>
            <div class="shame-detail">MRP: ₹{int(row['Highest MRP Shown'])} → Sold at ₹{int(row['Lowest Price Seen'])}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── FRAUD SCORE SPEEDOMETER ────────────────────────────
st.markdown('<div class="section-header">🎯 Fraud Score Meter — Select Any Product</div>', unsafe_allow_html=True)
st.caption("Score combines claimed discount % and MRP inflation. Above 50 = suspicious. Above 75 = highly manipulative.")

selected = st.selectbox("Choose a product to inspect:", summary["Product Name"].tolist())
row = summary[summary["Product Name"] == selected].iloc[0]

col_gauge, col_details = st.columns([1, 1])

with col_gauge:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=row["Fraud Score"],
        title={"text": f"Fraud Score", "font": {"color": "white", "size": 18}},
        delta={"reference": 50, "increasing": {"color": "#FF2B2B"}, "decreasing": {"color": "#21C354"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "white"},
            "bar": {"color": "#FF2B2B" if row["Fraud Score"] > 50 else "#21C354"},
            "bgcolor": "#1A1A1A",
            "bordercolor": "#333",
            "steps": [
                {"range": [0, 30], "color": "#0D2B0D"},
                {"range": [30, 60], "color": "#2B2B0D"},
                {"range": [60, 100], "color": "#2B0D0D"},
            ],
            "threshold": {
                "line": {"color": "#FF2B2B", "width": 4},
                "thickness": 0.75,
                "value": 50
            }
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="#0A0A0A",
        font={"color": "white"},
        height=300
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_details:
    st.markdown("<br><br>", unsafe_allow_html=True)
    verdict = "🚨 HIGHLY SUSPICIOUS" if row["Fraud Score"] > 60 else ("⚠️ SUSPICIOUS" if row["Fraud Score"] > 40 else "✅ LOOKS GENUINE")
    st.markdown(f"### {verdict}")
    st.markdown(f"**Highest MRP shown:** ₹{int(row['Highest MRP Shown'])}")
    st.markdown(f"**Lowest price seen:** ₹{int(row['Lowest Price Seen'])}")
    st.markdown(f"**Claimed discount:** {row['Claimed Discount %']}%")
    st.markdown(f"**MRP was inflated by:** {max(0, row['MRP Inflation %'])}%")
    st.markdown(f"**Category:** {row['Category']}")

st.markdown("---")

# ── PRICE HISTORY ──────────────────────────────────────
st.markdown('<div class="section-header">📈 Price History — Watch the Manipulation</div>', unsafe_allow_html=True)

product_df = df[df["Product Name"] == selected].sort_values("Date")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=product_df["Date"], y=product_df["MRP"],
    name="MRP (Crossed out price)",
    line=dict(color="#FF2B2B", dash="dash", width=2),
    mode="lines+markers",
    marker=dict(size=8)
))
fig2.add_trace(go.Scatter(
    x=product_df["Date"], y=product_df["Current Price"],
    name="Actual Selling Price",
    line=dict(color="#4FC3F7", width=3),
    mode="lines+markers",
    marker=dict(size=8),
    fill="tonexty",
    fillcolor="rgba(255,43,43,0.1)"
))
fig2.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#111111",
    font=dict(color="white"),
    xaxis=dict(gridcolor="#222"),
    yaxis=dict(gridcolor="#222", title="Price (₹)"),
    legend=dict(bgcolor="#1A1A1A", bordercolor="#333"),
    height=400,
    hovermode="x unified"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── CHART 1: All Products Bar ──────────────────────────
st.markdown('<div class="section-header">🚨 Claimed Discount % — All Products Ranked</div>', unsafe_allow_html=True)

fig1 = px.bar(
    summary.sort_values("Claimed Discount %"),
    x="Claimed Discount %",
    y="Product Name",
    color="Is Suspicious",
    color_discrete_map={True: "#FF2B2B", False: "#21C354"},
    orientation="h",
    text="Claimed Discount %",
    height=600
)
fig1.update_traces(texttemplate="%{text}%", textposition="outside")
fig1.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#111111",
    font=dict(color="white"),
    xaxis=dict(gridcolor="#222"),
    yaxis=dict(gridcolor="#222"),
    legend_title="Suspicious",
    showlegend=True,
    xaxis_title="Claimed Max Discount %",
    yaxis_title=""
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ── CHART 2: Category ──────────────────────────────────
st.markdown('<div class="section-header">📦 Category Breakdown — Who Cheats the Most?</div>', unsafe_allow_html=True)

cat_summary = summary.groupby("Category")["Claimed Discount %"].mean().round(1).reset_index()
cat_summary = cat_summary.sort_values("Claimed Discount %", ascending=False)

fig3 = px.bar(
    cat_summary,
    x="Category",
    y="Claimed Discount %",
    color="Claimed Discount %",
    color_continuous_scale=["#21C354", "#FFA500", "#FF2B2B"],
    text="Claimed Discount %",
    height=400
)
fig3.update_traces(texttemplate="%{text}%", textposition="outside")
fig3.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#111111",
    font=dict(color="white"),
    xaxis=dict(gridcolor="#222"),
    yaxis=dict(gridcolor="#222"),
    coloraxis_showscale=False
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── CHART 3: Scatter ───────────────────────────────────
st.markdown('<div class="section-header">💰 MRP vs Actual Price — The Smoking Gun</div>', unsafe_allow_html=True)
st.caption("If every discount were real, all dots would sit on the diagonal line. Dots far below the line = suspicious.")

fig4 = px.scatter(
    summary,
    x="Highest MRP Shown",
    y="Lowest Price Seen",
    color="Fraud Score",
    size="Claimed Discount %",
    hover_name="Product Name",
    color_continuous_scale=["#21C354", "#FFA500", "#FF2B2B"],
    text="Product Name",
    height=500
)
fig4.update_traces(textposition="top center")
fig4.add_shape(
    type="line", x0=0, y0=0,
    x1=summary["Highest MRP Shown"].max(),
    y1=summary["Highest MRP Shown"].max(),
    line=dict(color="#444", dash="dot", width=2)
)
fig4.add_annotation(
    x=summary["Highest MRP Shown"].max() * 0.8,
    y=summary["Highest MRP Shown"].max() * 0.85,
    text="Fair pricing line",
    font=dict(color="#666", size=11),
    showarrow=False
)
fig4.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#111111",
    font=dict(color="white"),
    xaxis=dict(gridcolor="#222", title="Highest MRP Shown (₹)"),
    yaxis=dict(gridcolor="#222", title="Lowest Price Seen (₹)")
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#555; font-size:13px; padding:20px">
    <b style="color:#FF2B2B">METHODOLOGY</b> — Prices tracked daily using Python (requests + BeautifulSoup + ScraperAPI). 
    A product is flagged suspicious when claimed discount exceeds 50%, indicating potential MRP inflation.<br><br>
    Built by <b style="color:#FF2B2B">Muskan Varma</b> | Data: Apr 22–25, 2026 | 
    <a href="https://github.com/muskanvarmaa" style="color:#FF2B2B">GitHub</a>
</div>
""", unsafe_allow_html=True)