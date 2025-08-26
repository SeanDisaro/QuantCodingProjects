import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np



def get_SP500_Symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    payload = pd.read_html(response.text)
    sp500_table = payload[0]
    return list(sp500_table.Symbol)




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


