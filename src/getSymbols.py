import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np



def get_SP500_Symbols():
    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(URL)

    sp500_Symbols = list(tables[0]["Symbol"]) 
    return sp500_Symbols




def get_SP500_ByIndustries():

    sp500_Symbols = get_SP500_Symbols()

    data = pd.DataFrame(columns=('symbol', 'industry'))

    for i in range(len(sp500_Symbols)):
        symb = sp500_Symbols[i]
        stock = yf.Ticker(symb)
        info = stock.get_info()
        try:
            data.loc[i] = [symb,info["industry"]]
        except:
            print("industry not found for "+ symb)


    data_grouped_by_industry = [group.reset_index() for _, group in data.groupby('industry')]

    return data_grouped_by_industry


