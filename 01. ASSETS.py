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