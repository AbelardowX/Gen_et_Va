import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
import plotly.express as px
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)

st.set_page_config(page_title="Gen et Va – Commodity Monitor", layout="wide")

st.title("Gen et Va")
st.subheader("Commodity Market Monitoring & Trade Support")

# ------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_commodities(start="2010-01-01"):
    tickers = ['BZ=F', 'CC=F', 'CL=F', 'GC=F', 'HG=F', 'KC=F', 'NG=F', 'ZS=F']
    data = yf.download(tickers, start=start, end=date.today(), auto_adjust=True, progress=False)['Close']
    data.columns = ['Brent', 'Cocoa', 'WTI', 'Gold', 'Copper', 'Coffee', 'Natgas', 'Soybean']
    return data

assets = load_commodities()

# Returns
returns = assets.copy()
for col in assets.columns:
    returns[f'{col}_Return'] = returns[col].pct_change()
    returns[f'{col}_Log_Return'] = np.log(returns[col] / returns[col].shift(1))
returns.dropna(inplace=True)

# Volatility
vol_cols = [c for c in returns.columns if c.endswith('_Log_Return')]
volatility = returns[vol_cols].copy()
for col in vol_cols:
    volatility[f'{col}_Volatility-30D'] = volatility[col].rolling(30).std() * np.sqrt(252)
    volatility[f'{col}_Volatility-90D'] = volatility[col].rolling(90).std() * np.sqrt(252)
volatility.dropna(inplace=True)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
section = st.sidebar.radio(
    "Section",
    ["Overview", "Energy", "Metals", "Soft Commodities", "Key Findings"]
)

# ------------------------------------------------------------------
# OVERVIEW
# ------------------------------------------------------------------
if section == "Overview":
    st.header("Price Overview")
    st.plotly_chart(px.line(assets, title="Commodity Prices"), use_container_width=True)

    st.subheader("Latest prices")
    st.dataframe(assets.tail(5).style.format("{:.2f}"), use_container_width=True)

# ------------------------------------------------------------------
# ENERGY
# ------------------------------------------------------------------
elif section == "Energy":
    st.header("Energy – Brent, WTI & Natural Gas")

    energy = assets[['Brent', 'WTI', 'Natgas']].copy()
    energy['Spread'] = energy['Brent'] - energy['WTI']

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Brent – WTI Spread (latest)", f"{energy['Spread'].iloc[-1]:.2f}")
    with col2:
        st.write(energy['Spread'].describe().to_frame().T)

    st.subheader("Brent vs WTI Spread")
    st.plotly_chart(px.line(energy['Spread'], title="Brent – WTI Spread"), use_container_width=True)

    # Natgas seasonality
    st.subheader("Natural Gas Seasonality")
    natgas_returns_month = returns.groupby(returns.index.month)['Natgas_Return'].mean().to_frame()
    st.plotly_chart(px.line(natgas_returns_month, title="Natgas Average Returns by Month"), use_container_width=True)

    natgas_vol_month = volatility.groupby(volatility.index.month)['Natgas_Log_Return_Volatility-30D'].mean().to_frame()
    st.plotly_chart(px.line(natgas_vol_month, title="Natgas Average 30D Volatility by Month"), use_container_width=True)

    natgas_price_month = assets.groupby(assets.index.month)['Natgas'].mean().to_frame()
    st.plotly_chart(px.line(natgas_price_month, title="Natgas Average Price by Month"), use_container_width=True)

    # Drawdowns
    st.subheader("Drawdowns")
    for name, ret_col in [("Brent", "Brent_Return"), ("Natgas", "Natgas_Return")]:
        cum = (1 + returns[ret_col]).cumprod()
        dd = (cum - cum.cummax()) / cum.cummax()
        st.plotly_chart(px.line(dd, title=f"{name} Drawdown"), use_container_width=True)

    # Correlation
    st.subheader("Correlation")
    corr = energy[['Brent', 'WTI', 'Natgas']].corr()
    st.plotly_chart(px.imshow(corr, text_auto=".2f", title="Energy Correlation"), use_container_width=True)

# ------------------------------------------------------------------
# METALS
# ------------------------------------------------------------------
elif section == "Metals":
    st.header("Metals – Gold & Copper")

    metals = assets[['Gold', 'Copper']].copy()
    metals['Gold/Copper'] = metals['Gold'] / metals['Copper']
    metals['Copper/Gold'] = metals['Copper'] / metals['Gold']

    st.plotly_chart(px.line(metals['Gold/Copper'], title="Gold / Copper Ratio"), use_container_width=True)
    st.plotly_chart(px.line(metals['Copper/Gold'], title="Copper / Gold Ratio"), use_container_width=True)

    st.subheader("Drawdowns")
    for name, ret_col in [("Gold", "Gold_Return"), ("Copper", "Copper_Return")]:
        cum = (1 + returns[ret_col]).cumprod()
        dd = (cum - cum.cummax()) / cum.cummax()
        st.plotly_chart(px.line(dd, title=f"{name} Drawdown"), use_container_width=True)

    st.subheader("Correlation")
    corr = metals[['Gold', 'Copper']].corr()
    st.plotly_chart(px.imshow(corr, text_auto=".2f", title="Metals Correlation"), use_container_width=True)

# ------------------------------------------------------------------
# SOFT COMMODITIES
# ------------------------------------------------------------------
elif section == "Soft Commodities":
    st.header("Soft Commodities – Cocoa, Coffee, Soybean")

    st.subheader("Returns")
    st.plotly_chart(
        px.line(returns[['Cocoa_Return', 'Coffee_Return', 'Soybean_Return']], title="Soft Commodity Returns"),
        use_container_width=True
    )

    soft_vola = volatility[[
        'Cocoa_Log_Return_Volatility-30D',
        'Coffee_Log_Return_Volatility-30D',
        'Soybean_Log_Return_Volatility-30D'
    ]]
    st.plotly_chart(px.line(soft_vola, title="Soft Commodities 30D Volatility"), use_container_width=True)

    # Seasonality tabs
    tab1, tab2, tab3 = st.tabs(["Cocoa", "Coffee", "Soybean"])

    with tab1:
        st.plotly_chart(
            px.line(returns.groupby(returns.index.month)['Cocoa_Return'].mean().to_frame(),
                    title="Cocoa Avg Returns by Month"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(volatility.groupby(volatility.index.month)['Cocoa_Log_Return_Volatility-30D'].mean().to_frame(),
                    title="Cocoa Avg Volatility by Month"),
            use_container_width=True
        )
        # Current vol
        curr = volatility['Cocoa_Log_Return_Volatility-30D'].iloc[-1]
        max_vol = volatility['Cocoa_Log_Return_Volatility-30D'].max()
        st.metric("Cocoa Current 30D Vol vs Historical Max", f"{curr/max_vol*100:.1f}%")

    with tab2:
        st.plotly_chart(
            px.line(returns.groupby(returns.index.month)['Coffee_Return'].mean().to_frame(),
                    title="Coffee Avg Returns by Month"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(volatility.groupby(volatility.index.month)['Coffee_Log_Return_Volatility-30D'].mean().to_frame(),
                    title="Coffee Avg Volatility by Month"),
            use_container_width=True
        )

    with tab3:
        st.plotly_chart(
            px.line(returns.groupby(returns.index.month)['Soybean_Return'].mean().to_frame(),
                    title="Soybean Avg Returns by Month"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(volatility.groupby(volatility.index.month)['Soybean_Log_Return_Volatility-30D'].mean().to_frame(),
                    title="Soybean Avg Volatility by Month"),
            use_container_width=True
        )

    st.subheader("Drawdowns")
    for name, ret_col in [("Cocoa", "Cocoa_Return"), ("Coffee", "Coffee_Return")]:
        cum = (1 + returns[ret_col]).cumprod()
        dd = (cum - cum.cummax()) / cum.cummax()
        st.plotly_chart(px.line(dd, title=f"{name} Drawdown"), use_container_width=True)

    st.subheader("Correlation")
    corr = assets[['Cocoa', 'Coffee', 'Soybean']].corr()
    st.plotly_chart(px.imshow(corr, text_auto=".2f", title="Soft Commodities Correlation"), use_container_width=True)

# ------------------------------------------------------------------
# KEY FINDINGS
# ------------------------------------------------------------------
else:
    st.header("Key Findings")
    st.markdown("""
- **Brent** maintains a persistent premium over **WTI** (correlation ≈ 97%).
- **Natural Gas** shows strong seasonal volatility (peaks in winter).
- **Gold** and **Copper** are highly correlated (~80%); the market still leans risk-off.
- **Cocoa** is the most volatile soft commodity.
- Soybean returns tend to weaken in August.
- Cocoa experienced a notable drawdown in early 2026.
- Current Cocoa 30-day volatility is elevated relative to its historical maximum.
- Cross-commodity relationships remain useful monitoring tools for trading & middle-office support.
    """)

st.caption("Data source: Yahoo Finance • Never insult the hand of nature that bore you by becoming common.")