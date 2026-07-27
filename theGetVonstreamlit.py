import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
import plotly.express as px
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)

st.set_page_config(page_title="Gen et Va", layout="wide")

# ------------------------------------------------------------------
# Sidebar navigation (the only new thing)
# ------------------------------------------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to section:",
    [
        "Home / Introduction",
        "Assets",
        "Energy",
        "Metals",
        "Soft Commodities",
        "Key Findings"
    ]
)

# ------------------------------------------------------------------
# Shared data loading (cached)
# ------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_data():
    tickers = ['BZ=F', 'CC=F', 'CL=F', 'GC=F', 'HG=F', 'KC=F', 'NG=F', 'ZS=F']
    data = yf.download(tickers, start='2010-01-01', end=date.today(),
                       auto_adjust=True, progress=False)['Close']
    data.columns = ['Brent', 'Cocoa', 'WTI', 'Gold', 'Copper', 'Coffee', 'Natgas', 'Soybean']
    return data

assets = load_data()

returns = assets.copy()
for a in returns.columns:
    returns[f'{a}_Return'] = returns[a].pct_change(1)
    returns[f'{a}_Log_Return'] = np.log(returns[a] / returns[a].shift(1))
returns.dropna(inplace=True)

volatility = returns[[
    'Brent_Log_Return', 'Cocoa_Log_Return', 'WTI_Log_Return', 'Gold_Log_Return',
    'Copper_Log_Return', 'Coffee_Log_Return', 'Natgas_Log_Return', 'Soybean_Log_Return'
]].copy()

for a in list(volatility.columns):
    volatility[f'{a}_Volatility-30D'] = volatility[a].rolling(window=30).std() * np.sqrt(252)
    volatility[f'{a}_Volatility-90D'] = volatility[a].rolling(window=90).std() * np.sqrt(252)
volatility.dropna(inplace=True)

# ------------------------------------------------------------------
# HOME / INTRODUCTION
# ------------------------------------------------------------------
if section == "Home / Introduction":
    st.title("Gen et Va")
    st.subheader("Commodity Market Monitoring & Trade Support")

    st.markdown("""
    1. Project Overview
    

Gen et Va is a commodity market monitoring and trade support platform designed for energy, metals, and agricultural futures. It automates market monitoring by calculating risk metrics, cross-market relationships, and seasonality while providing an interactive dashboard for market analysi    s    .

The project was built to simulate the analytical workflow of a Trading Assistant or Middle Office Analyst in a commodity trading environm    e    n    t.


2. Obj    e    ctives

The project         aims to:

Monitor commodity markets aut    omatically.
Analyze volatili    ty and risk.
Compare relationships between     commodities.
Identify unusual mar    ket behaviour.
Support market monitoring through interactive     v    isualizations.

3. Co    m    modities         Covered

Ene    rgy:

WTI Crud    e Oil
Brent         Crude Oi    l    
Nat    ural Ga    s    

Metals:

Gol    d    
Coppe    r

S    oft Comm    o    d    ities:

Co    f    fee
Cocoa
Soybe    a    n


4. Feat    ures

Mark    et Analysis:

Dai    ly returns
Log ret    u    rns
Cumulative returns        
Rolling volatili    ty

Cross-Market     Analysis:

Brent    -    WTI spread
Gold-    C    opper rati    o    
Correlation         matrix

Risk M    onitoring:

Drawd    owns

Seasonalit    y    :

Monthl    y     returns
Monthly v    olatility
Seas    onal patterns    

Dashboard:

Inte    r    active charts
Ma    r    ket sum    m    ary
Ri    s    k over    v    iew
Comm    o    dity co    m    parison

    5    . Technolo    g    i    e    s:

Python

p    a    ndas

NumPy

yfinance

Plotly

Matplotlib

Streamlit



6. Ke    y     Insights:

During the analysis several inter    esting market behaviours were identified:

Brent     consistently traded at a premium to WTI.
Natural G    as exhibited strong seasonal volatility.
Gold and Copper showed periods of high c    o    rrelation.
Cocoa displa    y    ed the highest realized volatility amo    ngst the analyzed commo    dities.

7. Future I    mprovements:

Incorporate physical market         datasets.
Add anomaly     d    etection.
Connect to live APIs.
Include inventory and weather information.

8. About this Project:

This project was developed to strengthen my technical and market knowledge while preparing for Trading Assistant and Middle Office roles within commodity trading houses.the hand of nature that bore you by becoming common.
Greatness is awaken and the GOAT is within YOU.
Abelardo

    """)

# ------------------------------------------------------------------
# ASSETS
# ------------------------------------------------------------------
elif section == "Assets":
    st.header("Assets")
    st.dataframe(assets, use_container_width=True)

# ------------------------------------------------------------------
# RETURNS
# ------------------------------------------------------------------
elif section == "Returns":
    st.header("Returns")
    st.dataframe(returns, use_container_width=True)

# ------------------------------------------------------------------
# VOLATILITY
# ------------------------------------------------------------------
elif section == "Volatility":
    st.header("Volatility")
    st.dataframe(volatility, use_container_width=True)

# ------------------------------------------------------------------
# ENERGY 
# ------------------------------------------------------------------
elif section == "Energy":
    st.header("Energy")

    st.markdown("""
    Energy commodities are strongly influenced by regional supply dynamics, transportation, weather and geopolitical events.  

    This section studies the relationships between Brent, WTI and Natural Gas.
    """)

    energy = assets[['Brent', 'WTI', 'Natgas']].copy()
    st.dataframe(energy, use_container_width=True)

    st.subheader("Spread: Brent VS WTI")
    energy['Spread'] = energy['Brent'] - energy['WTI']
    st.dataframe(energy['Spread'].describe().to_frame().T, use_container_width=True)

    st.markdown("""
    Brent still trading at premium comparing to WTI, with Hormuz, closed the international benchmark 
    takes the lead with an average of 6.07 of difference.
    """)

    st.subheader("Natgas")
    st.markdown("### Seasonality")

    natgas_returns_month = returns.groupby(returns.index.month)['Natgas_Return'].mean().to_frame()
    st.dataframe(natgas_returns_month, use_container_width=True)
    st.plotly_chart(px.line(natgas_returns_month, title='Natgas Returns by Month'), use_container_width=True)

    st.markdown("Natgas returns drops in December however it strengthens in February.")

    st.markdown("#### Volatility")
    natgas_volatility_month = volatility.groupby(volatility.index.month)['Natgas_Log_Return_Volatility-30D'].mean().to_frame()
    st.dataframe(natgas_volatility_month, use_container_width=True)
    st.plotly_chart(px.line(natgas_volatility_month, title='Natgas Volatility by Month'), use_container_width=True)

    st.markdown("Natgas volatilty peaks in winter months, starting in September and falls down in April.")

    st.markdown("#### Patterns")
    natgas_price_patterns = assets.groupby(assets.index.month)['Natgas'].mean().to_frame()
    st.dataframe(natgas_price_patterns, use_container_width=True)
    st.plotly_chart(px.line(natgas_price_patterns, title='Natgas Price Patterns by Month'), use_container_width=True)

    st.markdown("""
    Natgas price has a clear pattern to be at its highest in November and falls back in March, 
    then starts creating its momentum in April to peak in Winter again.
    """)

    st.subheader("Drawdown")

    st.markdown("### Brent")
    brent_cumulative_return = (1 + returns['Brent_Return']).cumprod()
    brent_cumulative_max = brent_cumulative_return.cummax()
    brent_drawdown = (brent_cumulative_return - brent_cumulative_max) / brent_cumulative_max
    st.plotly_chart(px.line(brent_drawdown, title='Brent Drawdown'), use_container_width=True)

    st.markdown("Brent has only two periods of drawdown, first in January 2016 and March 2020 which is the most profund.")

    st.markdown("### Natgas")
    natgas_cumulative_return = (1 + returns['Natgas_Return']).cumprod()
    natgas_cumulative_max = natgas_cumulative_return.cummax()
    natgas_drawdown = (natgas_cumulative_return - natgas_cumulative_max) / natgas_cumulative_max
    st.plotly_chart(px.line(natgas_drawdown, title='Natgas Drawdown'), use_container_width=True)

    st.markdown("""
    Natgas has three periods of drawdowns with an interval of 4 years, its first was in March 2016, 
    followed by June 2020 and the lastest in April 2024
    """)

    st.subheader("Correlation")
    corr_energy = energy[['Brent', 'WTI', 'Natgas']].corr()
    st.plotly_chart(px.imshow(corr_energy, text_auto=True, title='Correlation in Energy'), use_container_width=True)

    st.markdown("""
    Here we can see that both international benchmarks have a correlation of 97%, 
    however Natgas is correlated with Brent in 45% and 51% with WTI.
    """)

# ------------------------------------------------------------------
# METALS 
# ------------------------------------------------------------------
elif section == "Metals":
    st.header("METALS")

    st.markdown("""
    Metals are the foundation for technological advancement and global growth.  
    Geologic conditions, technology, economy, resource ownership and its concentration, 
    metallurgy are major areas that determine the supply of metals.  
    This section studies the relationships between precious metals and base metals.
    """)

    metals = assets[['Gold', 'Copper']].copy()
    st.dataframe(metals, use_container_width=True)

    st.subheader("Ratio: GOLD VS COPPER")
    metals['Ratio'] = metals['Gold'] / metals['Copper']
    st.dataframe(metals, use_container_width=True)
    st.plotly_chart(px.line(metals['Ratio'], title='Ratio: Gold / Copper'), use_container_width=True)

    st.markdown("""
    Copper is largely outperformed by Gold, usually the typical reasons are financial uncertainty 
    and less confidence in economy growth.
    """)

    ratio = metals['Copper'] / metals['Gold']
    st.plotly_chart(px.line(ratio, title='Ratio: Copper / Gold'), use_container_width=True)

    st.markdown("""
    Copper represents global demand, its higher price reflects economy progress, 
    we can see that it's been falling with intervals since 2011.
    """)

    st.subheader("Drawdown")

    st.markdown("### Gold")
    gold_cumulative_return = (1 + returns['Gold_Return']).cumprod()
    gold_cumulative_max = gold_cumulative_return.cummax()
    gold_drawdown = (gold_cumulative_return - gold_cumulative_max) / gold_cumulative_max
    st.plotly_chart(px.line(gold_drawdown, title='Gold Drawdown'), use_container_width=True)

    st.markdown("Gold has a long period of drawdown from June 2013 to October 2018.")

    st.markdown("### Copper")
    copper_cumulative_return = (1 + returns['Copper_Return']).cumprod()
    copper_cumulative_max = copper_cumulative_return.cummax()
    copper_drawdown = (copper_cumulative_return - copper_cumulative_max) / copper_cumulative_max
    st.plotly_chart(px.line(copper_drawdown, title='Copper Drawdown'), use_container_width=True)

    st.markdown("Copper has a long period of drawdown from January 2016 to March 2020.")

    st.subheader("Correlation")
    corr_metals = metals[['Gold', 'Copper']].corr()
    st.plotly_chart(px.imshow(corr_metals, text_auto=True, title='Correlation in Metals'), use_container_width=True)

    st.markdown("Both metals are correlated by 80%.")

# ------------------------------------------------------------------
# SOFT COMMODITIES (your original content, untouched)
# ------------------------------------------------------------------
elif section == "Soft Commodities":
    st.header("Soft Commodities")

    st.markdown("""
    Soft commodities are agricultural products, they are essential to global trade. 
    Softs are influenced by external factors like weather, pests, soil health, and geopolitical issues, 
    that can lead to higher price volatility. This section studies the relationships between them.
    """)

    softies = assets[['Cocoa', 'Coffee', 'Soybean']].copy()
    st.dataframe(softies, use_container_width=True)

    st.subheader("Softies Returns")
    st.plotly_chart(
        px.line(returns[['Cocoa_Return', 'Coffee_Return', 'Soybean_Return']]),
        use_container_width=True
    )

    st.subheader("Seasonality")

    st.markdown("### Cocoa")
    st.markdown("#### Returns")
    cocoa_returns_month = returns.groupby(returns.index.month)['Cocoa_Return'].mean().to_frame()
    st.plotly_chart(px.line(cocoa_returns_month, title='Cocoa Returns by Month for 16 years'), use_container_width=True)
    st.markdown("Cocoa tends to find higher returns in March and peaks in April.")

    st.markdown("#### Volatility")
    soft_vola = volatility[[
        'Cocoa_Log_Return_Volatility-30D',
        'Coffee_Log_Return_Volatility-30D',
        'Soybean_Log_Return_Volatility-30D'
    ]]
    st.plotly_chart(px.line(soft_vola, title='Soft Commodities Volatility'), use_container_width=True)
    st.markdown("Cocoa is the most volatile soft commodity.")

    cocoa_volatility_month = volatility.groupby(volatility.index.month)['Cocoa_Log_Return_Volatility-30D'].mean().to_frame()
    st.plotly_chart(px.line(cocoa_volatility_month, title='Cocoa Volatility by Month for 16 years'), use_container_width=True)
    st.markdown("For the last 16 years Cocoa tends to be more volatile mid November and be at its highest mid May.")

    st.dataframe(volatility['Cocoa_Log_Return_Volatility-30D'].describe().to_frame().T, use_container_width=True)

    current_volatility = volatility['Cocoa_Log_Return_Volatility-30D'].iloc[-1] / volatility['Cocoa_Log_Return_Volatility-30D'].max() * 100
    st.write(f"Cocoa Current Volatility %: {current_volatility:.1f}")

    st.markdown("""
    With the announcement of a possible El Niño coming in August until November by WMO, 
    Cocoa volaitility peaks at 63% at this moment; Cocoa prices are heavily influenced by 
    West African crop conditions and weather patterns.
    """)

    st.markdown("### Coffee")
    st.markdown("#### Seasonality")
    st.markdown("##### Returns")
    coffee_returns_month = returns.groupby(returns.index.month)['Coffee_Return'].mean().to_frame()
    st.dataframe(coffee_returns_month, use_container_width=True)
    st.plotly_chart(px.line(coffee_returns_month, title='Coffee Returns by Month'), use_container_width=True)
    st.markdown("Coffee returns drops in May after its peak in April,then goes to its highest peak in November.")

    st.markdown("##### Volatility")
    coffee_volatility_month = volatility.groupby(volatility.index.month)['Coffee_Log_Return_Volatility-30D'].mean().to_frame()
    st.dataframe(coffee_volatility_month, use_container_width=True)
    st.plotly_chart(px.line(coffee_volatility_month, title='Coffee Volatility by Month'), use_container_width=True)
    st.markdown("Coffee hightest volatility tends to be in July and its lowest in February")

    st.markdown("### Soybean")
    st.markdown("#### Returns")
    soybean_returns_month = returns.groupby(returns.index.month)['Soybean_Return'].mean().to_frame()
    st.dataframe(soybean_returns_month, use_container_width=True)
    st.plotly_chart(px.line(soybean_returns_month, title='Soybean Returns by Month'), use_container_width=True)
    st.markdown("Soybean returns have a tendency to drop in August.")

    st.markdown("#### Volatility")
    soybean_volatility_month = volatility.groupby(volatility.index.month)['Soybean_Log_Return_Volatility-30D'].mean().to_frame()
    st.dataframe(soybean_volatility_month, use_container_width=True)
    st.plotly_chart(px.line(soybean_volatility_month, title='Soybean Volatility by Month'), use_container_width=True)
    st.markdown("For the past 16 years Soybean tends to peak in volatility in August and drops in October before restarting the cycle.")

    st.subheader("Drawdown")

    st.markdown("### Cocoa")
    cocoa_cumulative_return = (1 + returns['Cocoa_Return']).cumprod()
    cocoa_cumulative_max = cocoa_cumulative_return.cummax()
    cocoa_drawdown = (cocoa_cumulative_return - cocoa_cumulative_max) / cocoa_cumulative_max
    st.plotly_chart(px.line(cocoa_drawdown, title='Cocoa Drawdown'), use_container_width=True)
    st.markdown("Cocoa experienced its first deep drawdown in the last days of February of 2026.")

    st.markdown("### Coffee")
    coffee_cumulative_return = (1 + returns['Coffee_Return']).cumprod()
    coffee_cumulative_max = coffee_cumulative_return.cummax()
    coffee_drawdown = (coffee_cumulative_return - coffee_cumulative_max) / coffee_cumulative_max
    st.plotly_chart(px.line(coffee_drawdown, title='Coffee Drawdown'), use_container_width=True)
    st.markdown("""
    Coffee spends its time in drawdown, its been there since November 2013 with a brief interval in 2015 
    and came back in January 2016, experiencing its deepest in October 2019, before leaving, aparently, for 'good'.
    """)

    st.subheader("Correlation")
    corr_softies = softies.corr()
    st.plotly_chart(px.imshow(corr_softies, text_auto=True, title='Correlation in Softies'), use_container_width=True)

    st.markdown("""
    Cocoa is negatively correlated with Soybean by -13%, and 66% with Coffee, 
    however Soybean is correlated with Coffee by 20%.
    """)

# ------------------------------------------------------------------
# KEY FINDINGS
# ------------------------------------------------------------------
elif section == "Key Findings":
    st.header("Key Findings")

    st.markdown("""
    • Brent maintains a persistent premium over WTI and both are correlated by 97%.

    • Natural Gas exhibits strong seasonal volatility.

    • Gold and Copper maintain a high positive correlation and the market is still lead by fear.

    • Cocoa is the most volatile soft commodity.

    • Soybean returns tends to drop in August.

    • Cocoa first drawdown was in February of 2026.

    • Cocoa volatility is 63% today.

    • Commodity relationships provide useful market monitoring indicators for trading support.
    """)

   
    
    
    st.markdown("""
    ##### Never insult the hand of nature that bore you by becoming common.
    ###### Greatness is awaken and the GOAT is within YOU.
    """)

    st.markdown("""
    Abelardo
    """)