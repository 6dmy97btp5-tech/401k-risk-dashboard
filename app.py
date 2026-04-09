# ============================================================
# 401(k) Alternative Investment Risk Analysis Dashboard
# Built by Ravell | LPL Financial — Annuities Trading Dept
# Tech stack: Python, yfinance, pandas, NumPy, Plotly, Streamlit
# ============================================================

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="401(k) Alternative Investment Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Header ───────────────────────────────────────────────────
st.title("📊 Alternative Investment 401(k) Risk Analysis Dashboard")
st.markdown(
    "Models **fee drag**, **correlation risk**, **liquidity scoring**, and "
    "**individual asset performance** across 5 asset classes commonly found "
    "in 401(k) alternative investment menus."
)
st.markdown("---")

# ── Tickers Dictionary ───────────────────────────────────────
TICKERS = {
    "SPY":  {"name": "SPDR S&P 500 ETF",                           "asset_class": "US Equity",        "type": "Traditional", "liquidity_score": 10, "expense_ratio": 0.0009},
    "AGG":  {"name": "iShares Core US Aggregate Bond ETF",          "asset_class": "Bonds",            "type": "Traditional", "liquidity_score": 9,  "expense_ratio": 0.0003},
    "VNQ":  {"name": "Vanguard Real Estate ETF",                    "asset_class": "Real Estate/REIT", "type": "Alternative", "liquidity_score": 7,  "expense_ratio": 0.0012},
    "PDBC": {"name": "Invesco Optimum Yield Diversified Commodity",  "asset_class": "Commodities",      "type": "Alternative", "liquidity_score": 6,  "expense_ratio": 0.0059},
    "BIL":  {"name": "SPDR Bloomberg 1-3 Month T-Bill ETF",         "asset_class": "Cash/Stable",      "type": "Traditional", "liquidity_score": 10, "expense_ratio": 0.0014}
}
tickers_list = list(TICKERS.keys())

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("Dashboard Settings")

period = st.sidebar.selectbox(
    "Select Analysis Period",
    options=["1y", "3y", "5y"],
    index=0,
    format_func=lambda x: {"1y": "1 Year", "3y": "3 Years", "5y": "5 Years"}[x]
)

st.sidebar.markdown("### Portfolio Allocation")
st.sidebar.markdown("Adjust weights below. Total must equal 100%.")

spy_weight  = st.sidebar.slider("SPY — US Equity",    0, 100, 40)
agg_weight  = st.sidebar.slider("AGG — Bonds",        0, 100, 20)
vnq_weight  = st.sidebar.slider("VNQ — Real Estate",  0, 100, 15)
pdbc_weight = st.sidebar.slider("PDBC — Commodities", 0, 100, 15)
bil_weight  = st.sidebar.slider("BIL — Cash/Stable",  0, 100, 10)

total_weight = spy_weight + agg_weight + vnq_weight + pdbc_weight + bil_weight

if total_weight != 100:
    st.sidebar.error(f"Total allocation is {total_weight}%. Must equal 100%.")
    st.warning("⚠️ Please adjust your portfolio allocation to equal 100% in the sidebar.")
    st.stop()
else:
    st.sidebar.success("✅ Allocation valid")

weights = {
    "SPY":  spy_weight  / 100,
    "AGG":  agg_weight  / 100,
    "VNQ":  vnq_weight  / 100,
    "PDBC": pdbc_weight / 100,
    "BIL":  bil_weight  / 100
}

# ── Data Fetch ────────────────────────────────────────────────
@st.cache_data(ttl=3600)  # cache data for 1 hour so app doesn't re-fetch on every interaction
def get_market_data(tickers, period="1y"):
    raw_data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    prices = raw_data["Close"]
    returns = prices.pct_change().dropna()
    corr_matrix = returns.corr()
    return prices, returns, corr_matrix

with st.spinner("Fetching live market data..."):
    prices, returns, corr_matrix = get_market_data(tickers_list, period)

# ── Fee Drag Calculation ──────────────────────────────────────
def calculate_fee_drag(initial_investment=100000,
                       annual_return=0.07,
                       years=30,
                       expense_ratios=[0.0003, 0.0025, 0.0050, 0.0075, 0.0100]):
    results = {}
    for ratio in expense_ratios:
        net_return = annual_return - ratio
        values = [initial_investment]
        for year in range(1, years + 1):
            new_value = values[-1] * (1 + net_return)
            values.append(new_value)
        label = f"{ratio*100:.2f}% expense ratio"
        results[label] = values

    baseline_key = f"{expense_ratios[0]*100:.2f}% expense ratio"
    drag_analysis = {}
    for label, values in results.items():
        if label != baseline_key:
            dollar_drag = results[baseline_key][-1] - values[-1]
            pct_drag = (dollar_drag / results[baseline_key][-1]) * 100
            drag_analysis[label] = {
                "final_value": values[-1],
                "dollar_drag": dollar_drag,
                "pct_drag": pct_drag
            }
    return results, drag_analysis

results, drag_analysis = calculate_fee_drag()

# ════════════════════════════════════════════════════════════
# SECTION 1 — FEE DRAG
# ════════════════════════════════════════════════════════════
st.markdown("## 💸 Section 1 — Fee Drag Analysis")
st.markdown(
    "How much does a higher expense ratio cost you over 30 years? "
    "Starting with **$100,000** at a **7% gross annual return**, "
    "the gap below is pure fee drag — wealth silently eroded by costs."
)

# Fee drag line chart
years_list = list(range(31))
fee_df = pd.DataFrame(results)
fee_df.insert(0, "Year", years_list)
fee_long = fee_df.melt(id_vars="Year", var_name="Expense Ratio", value_name="Portfolio Value")

fig_fee = px.line(
    fee_long,
    x="Year",
    y="Portfolio Value",
    color="Expense Ratio",
    title="Fee Drag Over 30 Years — $100,000 Initial Investment at 7% Gross Return",
    labels={"Portfolio Value": "Portfolio Value ($)", "Year": "Years Invested"},
    template="plotly_dark"
)
fig_fee.update_layout(yaxis_tickformat="$,.0f", hovermode="x unified", height=500)
st.plotly_chart(fig_fee, use_container_width=True)

# Fee drag summary metrics
st.markdown("### Fee Drag Summary")
cols = st.columns(len(drag_analysis))
for col, (label, data) in zip(cols, drag_analysis.items()):
    col.metric(
        label=label,
        value=f"${data['final_value']:,.0f}",
        delta=f"-${data['dollar_drag']:,.0f} ({data['pct_drag']:.1f}% lost)",
        delta_color="inverse"
    )

st.markdown("---")

# ════════════════════════════════════════════════════════════
# SECTION 2 — CORRELATION HEATMAP
# ════════════════════════════════════════════════════════════
st.markdown("## 🔗 Section 2 — Asset Correlation Risk")
st.markdown(
    "Correlation ranges from **-1** (assets move opposite) to **+1** (assets move together). "
    "Lower correlation across your holdings = better diversification = lower portfolio risk."
)

fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    title="Asset Correlation Matrix — Daily Returns",
    template="plotly_dark"
)
fig_corr.update_layout(height=500, coloraxis_colorbar=dict(title="Correlation"))
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════
# SECTION 3 — LIQUIDITY SCORING
# ════════════════════════════════════════════════════════════
st.markdown("## 💧 Section 3 — Liquidity Scoring")
st.markdown(
    "Liquidity score rates how quickly each holding can be exited without significant price impact. "
    "**10 = Most liquid** (can sell instantly). Alternative assets score lower due to market depth and structure."
)

liquidity_data = [
    {
        "Ticker": ticker,
        "Name": info["name"],
        "Asset Class": info["asset_class"],
        "Type": info["type"],
        "Liquidity Score": info["liquidity_score"],
        "Expense Ratio %": round(info["expense_ratio"] * 100, 3)
    }
    for ticker, info in TICKERS.items()
]
liquidity_df = pd.DataFrame(liquidity_data)

fig_liq = px.bar(
    liquidity_df,
    x="Ticker",
    y="Liquidity Score",
    color="Type",
    color_discrete_map={"Traditional": "#00CC96", "Alternative": "#EF553B"},
    title="Liquidity Score by Asset Class (10 = Most Liquid)",
    text="Liquidity Score",
    hover_data=["Name", "Expense Ratio %"],
    template="plotly_dark"
)
fig_liq.update_layout(yaxis_range=[0, 11], height=450, legend_title="Asset Type")
fig_liq.update_traces(textposition="outside")
st.plotly_chart(fig_liq, use_container_width=True)

st.markdown("### Liquidity & Cost Reference Table")
st.dataframe(
    liquidity_df[["Ticker", "Name", "Asset Class", "Type", "Liquidity Score", "Expense Ratio %"]],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ════════════════════════════════════════════════════════════
# SECTION 4 — INDIVIDUAL ASSET PERFORMANCE
# ════════════════════════════════════════════════════════════
st.markdown("## 📈 Section 4 — Individual Asset Performance")
st.markdown(
    "All assets normalized to a base of **100** at the start of the selected period. "
    "This removes price level differences so you can compare performance directly — apples to apples."
)

normalized_prices = (prices / prices.iloc[0]) * 100
normalized_prices.index.name = "Date"
normalized_long = normalized_prices.reset_index().melt(
    id_vars="Date",
    var_name="Ticker",
    value_name="Normalized Price"
)

fig_perf = px.line(
    normalized_long,
    x="Date",
    y="Normalized Price",
    color="Ticker",
    title="Normalized Asset Performance (Base = 100 at Start of Period)",
    labels={"Normalized Price": "Indexed Value (Start = 100)"},
    template="plotly_dark"
)
fig_perf.add_hline(y=100, line_dash="dash", line_color="gray", annotation_text="Starting baseline")
fig_perf.update_layout(height=500, hovermode="x unified")
st.plotly_chart(fig_perf, use_container_width=True)

# Stats table
st.markdown("### Performance Stats Summary")
stats_data = []
for t in tickers_list:
    total_return = round(float(normalized_prices[t].iloc[-1]) - 100, 2)
    ann_vol = round(float(returns[t].std()) * np.sqrt(252) * 100, 2)
    max_dd = round(float((prices[t] / prices[t].cummax() - 1).min()) * 100, 2)
    stats_data.append({
        "Ticker": t,
        "Asset Class": TICKERS[t]["asset_class"],
        "Type": TICKERS[t]["type"],
        "Total Return %": total_return,
        "Ann. Volatility %": ann_vol,
        "Max Drawdown %": max_dd
    })

stats_df = pd.DataFrame(stats_data)
st.dataframe(stats_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Dashboard built by Ravell | Data sourced from Yahoo Finance via yfinance | LPL Financial — Annuities Trading Department")
