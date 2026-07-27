import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import date



class Commodities:
    '''This extracts data from Commodities listed below. 
    Provide the day it will give you the data from that day until yesterday.
    The commodities are: Brent, Cocoa, Gold, Copper, Coffee, Natgas and Soybean'''
    def __init__ (self, start, asset=['BZ=F', 'CC=F', 'CL=F', 'GC=F', 'HG=F', 'KC=F', 'NG=F', 'ZS=F'], end = date.today()):
        self.asset = asset
        self.end = end
        self.start = start
        self.data = self.tickers()
    
    def tickers (self):
        data = yf.download(self.asset, self.start, self.end, auto_adjust=True).Close
        data.columns=['Brent', 'Cocoa', 'WTI', 'Gold', 'Copper', 'Coffee', 'Natgas', 'Soybean']
        return data





# Generated from: 02. Gen_et_Va.ipynb
# Converted at: 2026-07-27T07:38:41.577Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# # Gen et Va 
# 
# #### Commodity Market Monitoring & Trade Support 


# This project analyzes futures market across energy, metals, and agricultural commodities. It focuses on market monitoring, risk metrics, seasonality, cross-market relationships, and market intelligence for Trading Assistant and Middle Office workflows.


import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

# # Assets:


assets = Commodities('2010-01-01').data

assets

# # Returns


returns = assets.copy()

returns.head()

for a in returns:
    returns['{}_Return'.format(a)] = returns[a].pct_change(1)
    returns['{}_Log_Return'.format(a)] = np.log(returns[a]/returns[a].shift(1))

returns.dropna(inplace=True)
returns

# # Volatility


volatility = returns.copy()

volatility = volatility[['Brent_Log_Return','Cocoa_Log_Return', 'WTI_Log_Return','Gold_Log_Return', 'Copper_Log_Return', 'Coffee_Log_Return',
            'Natgas_Log_Return', 'Soybean_Log_Return']]

volatility

for a in volatility:
    volatility['{}_Volatility-30D'.format(a)] = volatility[a].rolling(window=30).std() * np.sqrt(252)
    volatility['{}_Volatility-90D'.format(a)] = volatility[a].rolling(window=90).std() * np.sqrt(252)

volatility.dropna(inplace=True)
volatility

# # Energy:


# Energy commodities are strongly influenced by
# regional supply dynamics, transportation,
# weather and geopolitical events.
# 
# This section studies the relationships
# between Brent, WTI and Natural Gas.


energy = assets[['Brent', 'WTI', 'Natgas']]

energy

# ## Spread: Brent VS WTI


energy['Spread'] = energy['Brent'] - energy['WTI']

energy.Spread.describe().to_frame().T

# Brent still trading at premium comparing to WTI, with Hormuz, closed the international benchmark takes the lead with an average of 6.07 of difference.


# ## Natgas


# ### Seasonality


natgas_returns_month = returns.groupby(returns.index.month)['Natgas_Return'].mean().to_frame()
natgas_returns_month

px.line(natgas_returns_month, title=('Natgas Returns by Month'), width=1100, height=500)

# Natgas returns drops in December however it strengthens in February.


# #### Volatility


natgas_volatility_month = volatility.groupby(volatility.index.month)['Natgas_Log_Return_Volatility-30D'].mean().to_frame()
natgas_volatility_month

px.line(natgas_volatility_month, title=('Natgas Volatility by Month'), width=1100, height=500)

# Natgas volatilty peaks in winter months, starting in September and falls down in April.


# #### Patterns


natgas_price_patterns = assets.groupby(assets.index.month)['Natgas'].mean().to_frame()
natgas_price_patterns

px.line(natgas_price_patterns, title=('Natgas Price Patterns by Month'), width=1100, height=500)

# Natgas price has a clear pattern to be at its highest in November and falls back in March, then starts creating its momentum in April to peak in Winter again. 


# # Drawdown


# ## Brent


brent_cumulative_return = (1 + returns['Brent_Return']).cumprod()
brent_cumulative_max = brent_cumulative_return.cummax()
brent_drawdown = (brent_cumulative_return - brent_cumulative_max)/brent_cumulative_max

bd = brent_drawdown.to_frame()

px.line(brent_drawdown, title=('Brent Drawdown'), width=1100, height=500)

# Brent has only two periods of drawdown, first in January 2016 and  March 2020 which is the most profund.


# ## Natgas


natgas_cumulative_return = (1 + returns['Natgas_Return']).cumprod()
natgas_cumulative_max = natgas_cumulative_return.cummax()
natgas_drawdown = (natgas_cumulative_return - natgas_cumulative_max) / natgas_cumulative_max

px.line(natgas_drawdown, title=('Natgas Drawdown'), width=1100, height=500)

# Natgas has three periods of drawdowns with an interval of 4 years, its first was in March 2016, followed by June 2020 and the lastest in April 2024


# ## Correlation


corr_energy = energy[['Brent', 'WTI', 'Natgas']].corr()

px.imshow(corr_energy, width=1000, height=800, text_auto=True, title=('Correlation in Energy'))

# Here we can see that both international benchmarks have a correlation of 97%, however Natgas is correlated with Brent in 45% and 51% with WTI.


# # METALS


# Metals are the foundation for technological advancement and global growth.
# Geologic conditions, technology, economy, resource ownership and its concentration, metallurgy are major areas that determine the supply of metals.
# This section studies the relationships between precious metals and base metals.


metals = assets[['Gold', 'Copper']].copy()

metals

# ### Ratio: GOLD VS COPPER


metals['Ratio'] = metals['Gold'] / metals['Copper']

metals

px.line(metals['Ratio'], title=('Ratio: Gold / Copper'), width=1100, height=500)

# Copper is largely outperformed by Gold, usually the typical reasons are financial uncertainty and less confidence in economy growth.


ratio = metals['Copper']/ metals['Gold']
px.line(ratio, title=('Ratio: Copper / Gold'), width=1100, height=500)

# Copper represents global demand, its higher price reflects economy progress, we can see that it's been falling with intervals since 2011.


# ## Drawdown


# ### Gold


gold_cumulative_return = (1 + returns['Gold_Return']).cumprod()
gold_cumulative_max = gold_cumulative_return.cummax()
gold_drawdown = (gold_cumulative_return - gold_cumulative_max) / gold_cumulative_max

px.line(gold_drawdown, title=('Gold Drawdown'), width=1100, height=500)

# Gold has a long period of drawdown from June 2013 to October 2018.


# ### Copper


copper_cumulative_return = (1 + returns['Copper_Return']).cumprod()
copper_cumulative_max = copper_cumulative_return.cummax()
copper_drawdown = (copper_cumulative_return - copper_cumulative_max) / copper_cumulative_max

px.line(copper_drawdown, title=('Copper Drawdown'), width=1100, height=500)

# Copper has a long period of drawdown from January 2016 to March 2020.


# ## Correlation


corr_metals = metals[['Gold', 'Copper']].corr()

px.imshow(corr_metals, width=1000, height=800, text_auto=True, title=('Correlation in Metals'))

# Both metals are correlated by 80%.


# # Soft Commodities


# Soft commodities are agricultural products, they are essential to global trade. Softs are influenced by external factors like weather, pests, soil health, and geopolitical issues, that can lead to higher price volatility. This section studies the relationships between them.


softies = assets[['Cocoa', 'Coffee', 'Soybean']].copy()

softies

# ### Softies Returns


px.line(returns[['Cocoa_Return', 'Coffee_Return', 'Soybean_Return']], width=1100, height=500)

# ## Seasonality


# ### Cocoa


# #### Returns


cocoa_returns_month = returns.groupby(returns.index.month)['Cocoa_Return'].mean().to_frame()

px.line(cocoa_returns_month, title=('Cocoa Returns by Month for 16 years'), width=1100, height=500)

# Cocoa tends to find higher returns in March and peaks in April.


# #### Volatility


soft_vola= volatility[['Cocoa_Log_Return_Volatility-30D', 'Coffee_Log_Return_Volatility-30D', 'Soybean_Log_Return_Volatility-30D']]

px.line(soft_vola, title=('Soft Commodities Volatility'),  width=1100, height=500)

# Cocoa is the most volatile soft commodity.


cocoa_volatility_month = volatility.groupby(volatility.index.month)['Cocoa_Log_Return_Volatility-30D'].mean().to_frame()

px.line(cocoa_volatility_month, title=('Cocoa Volatility by Month for 16 years'), width=1100, height=500)

# For the last 16 years Cocoa tends to be more volatile mid November and be at its highest mid May.


volatility['Cocoa_Log_Return_Volatility-30D'].describe().to_frame().T

current_volatility = volatility['Cocoa_Log_Return_Volatility-30D'][-1:] / volatility['Cocoa_Log_Return_Volatility-30D'].max() * 100
print(f'Cocoa Current Volatility %: {current_volatility}')

# With the announcement of a possible El Niño coming in August until November by WMO, Cocoa volaitility peaks at 63% at this moment; Cocoa prices are heavily influenced by West African crop conditions and weather patterns.


# ## Coffee


# ### Seasonality


# #### Returns


coffee_returns_month = returns.groupby(returns.index.month)['Coffee_Return'].mean().to_frame()
coffee_returns_month

px.line(coffee_returns_month, title=('Coffee Returns by Month'), width=1100, height=400)

# Coffee returns drops in May after its peak in April,then goes to its highest peak in November.


# #### Volatility


coffee_volatility_month = volatility.groupby(volatility.index.month)['Coffee_Log_Return_Volatility-30D'].mean().to_frame()
coffee_volatility_month

px.line(coffee_volatility_month, title=('Coffee Volatility by Month'), width=1100, height=400)

# Coffee hightest volatility tends to be in July and its lowest in February


# ### Soybean


# ### Returns


soybean_returns_month = returns.groupby(returns.index.month)['Soybean_Return'].mean().to_frame()
soybean_returns_month

px.line(soybean_returns_month, width=1100, height=400, title=('Soybean Returns by Month'))

# Soybean returns has tendency to drop in August.


# ### Volatility


soybean_volatility_month = volatility.groupby(volatility.index.month)['Soybean_Log_Return_Volatility-30D'].mean().to_frame()
soybean_volatility_month

px.line(soybean_volatility_month, width=1100, height=400, title=('Soybean Volatility by Month'))

# For the past 16 years Soybean tends to peak in volatility in August and drops in October before restarting the cycle.


# ## Drawdown


# ### Cocoa


cocoa_cumulative_return = (1 + returns['Cocoa_Return']).cumprod()
cocoa_cumulative_max = cocoa_cumulative_return.cummax()
cocoa_drawdown = (cocoa_cumulative_return - cocoa_cumulative_max) / cocoa_cumulative_max

px.line(cocoa_drawdown, title=('Cocoa Drawdown'), width=1100, height=500)

# Cocoa experienced its first deep drawdown in the lastest days of February of 2026.


# ### Coffee


coffee_cumulative_return = (1 + returns['Coffee_Return']).cumprod()
coffee_cumulative_max = coffee_cumulative_return.cummax()
coffee_drawdown = (coffee_cumulative_return - coffee_cumulative_max) / coffee_cumulative_max

px.line(coffee_drawdown, title=('Coffee Drawdown'), width=1100, height=500)

# Coffee spends its time in drawdown, its been there since November 2013 with a brief interval in 2015 and came back in January 2016, experiencing its deepest in October 2019, before leaving, aparently, for 'good'. 


# ## Correlation


corr_softies = softies.corr()

px.imshow(corr_softies, width=1000, height=800, text_auto=True, title=('Correlation in Softies'))

# Cocoa is negatively correlated with Soybean by -13%, and 66% with Coffee, however Soybean is correlated with Coffee by 20%. 


# # Key Findings


# • Brent maintains a persistent premium over WTI and both are correlated by 97%.
# 
# • Natural Gas exhibits strong seasonal volatility.
# 
# • Gold and Copper maintain a high positive correlation and the market is still lead by fear.
# 
# • Cocoa is the most volatile soft commodity.
# 
# • Soybean returns tends to drop in August.
# 
# • Cocoa first drawdown was in February of 2026.
# 
# • Cocoa volatility is 63% today.
# 
# • Commodity relationships provide useful market monitoring indicators for trading support.


# ##### Never insult the hand of nature that bore you by becoming common.
# 
# ###### Greatness is awaken and the GOAT is within YOU.
#