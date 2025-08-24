import pandas as pd
import numpy as np
from src.backtesting.strat import *
from tabulate import tabulate
from bokeh.plotting import figure, show
from bokeh.layouts import column


class Backtester:
    def __init__(self, assets: list[pd.DataFrame], myStrategy:Strategy, capital:float = 10000, comissions= 0.002):

        self.startCapital = capital
        self.assets = assets
        self.strategy = myStrategy
        self.comissions = comissions
        self.portfolioOverTime:list[list[int]] = []
        self.cashOverTime: pd.DataFrame =  pd.DataFrame(columns=["Cash"], index=pd.DatetimeIndex([], name="Date"))
        self.capitalOverTime: pd.DataFrame =  pd.DataFrame(columns=["Capital"], index=pd.DatetimeIndex([], name="Date"))
        self.finalCapital = 0
        self.numberTrades = 0 # this counts on how many dates a trade was done. If the strategy involves multiple trades at one date, then this is only counted as one trade.
        self.numAssets = len(assets)
        self.tradingDays = len(assets[0])

    def setCapital(self, capital):
        self.capital = capital

    def setComissions(self, comissions):
        self.comissions = comissions

    def costsRebalance(self, oldPortfolio, newPortfolio, pricesAssets)->float:
        capitalDifference = 0
        absDiff = 0
        for i in range(self.numAssets):
            numSharesBought = newPortfolio[i] - oldPortfolio[i]  
            capitalDifference +=  numSharesBought * pricesAssets[i]
            absDiff += np.abs(numSharesBought * pricesAssets[i]).item()

        return capitalDifference + absDiff *self.comissions # Portfolio balance difference + comission costs

    def portfolioValue(self, portfolio, pricesAssets)->float:
        value = 0
        for i in range(self.numAssets):
            value += portfolio[i] * pricesAssets[i]
        return value

    def liquidatePositions(self, portfolio, pricesAssets):
        value = self.portfolioValue(portfolio, pricesAssets)
        return value * (1 - self.comissions)

    def run(self):
        startDate = self.assets[0].iloc[0].name
        numDates = len(self.assets[0])
        startPortfolio = [0 ]*self.numAssets
        self.portfolioOverTime.append(startPortfolio)
        self.cashOverTime.loc[startDate] = self.startCapital
        self.capitalOverTime.loc[startDate] = self.startCapital

        for dateIdx in range(1, numDates -1 ):
            oldPortfolio = self.portfolioOverTime[-1]
            date = self.assets[0].iloc[dateIdx ].name
            assetsUpToStep = [asset.iloc[:dateIdx] for asset in self.assets]
            pricesAssets = [ (asset.iloc[-1]["High"].item() + asset.iloc[-1]["Low"].item())/2  for asset in assetsUpToStep]

            newPortfolio = self.strategy.updatePortfolio(oldPortfolio= oldPortfolio, cash=self.cashOverTime.iloc[-1]["Cash"], pricesAssets = pricesAssets, assets = assetsUpToStep)
            if newPortfolio == None:
                pass
            self.portfolioOverTime.append(newPortfolio)

            costsRebalance = self.costsRebalance(oldPortfolio, newPortfolio, pricesAssets)

            if costsRebalance != 0:
                self.numberTrades += 1

            newCash = self.cashOverTime.iloc[-1]["Cash"] - costsRebalance

            self.capitalOverTime.loc[date] = self.portfolioValue(newPortfolio, pricesAssets) + newCash

            self.cashOverTime.loc[date] = newCash

        assetsUpToStep = [asset.iloc[:-1] for asset in self.assets]
        pricesAssets = [ (asset.iloc[-1]["High"].item() + asset.iloc[-1]["Low"].item())/2  for asset in assetsUpToStep]
        self.finalCapital = self.cashOverTime.iloc[-1]["Cash"] + self.liquidatePositions(self.portfolioOverTime[-1], pricesAssets)

    def reportResults(self):
        volatility = np.log(self.capitalOverTime["Capital"] / self.capitalOverTime["Capital"].shift(1)).std() *np.sqrt(self.tradingDays)
        print(tabulate([[self.startCapital, self.finalCapital, self.finalCapital - self.startCapital , str( round((self.finalCapital  - self.startCapital)*100 /self.startCapital , 2)) + "%" , volatility, self.numberTrades, self.tradingDays ]],
                         headers=["Start Capital", "Final Capital","Absolute Gains","Relative Gains", "Volatility (via log returns)", "Number Of Dates With Trades", "Number Trading Days" ]
                         )
                         )


    def plot(self):
        height=450
        width=1600
        #plot stocks
        stocksFigure = figure(
                x_axis_type="datetime",
                height = height,
                width = width,
                title="Stock Price Candlestick Chart",
                tools="pan,wheel_zoom,box_zoom,reset,save",
                x_axis_label="Date",
                y_axis_label="Price (USD)"
                )
        stocksFigure.xaxis.major_label_orientation = 0.8
        
        for i in range(self.numAssets):
            asset = self.assets[i]
            asset["status"] = ["up" if c >= o else "down" for c, o in zip(asset.Close, asset.Open)]
            asset_up = asset[asset.status == 'up']
            asset_down = asset[asset.status == 'down']
            bar_width_ms = 12 * 60 * 60 * 1000*2
            stocksFigure.segment(asset.index, asset.High, asset.index, asset.Low, color="black")
            stocksFigure.vbar(
                x=asset_up.index,
                width=bar_width_ms,
                top=asset_up.Close,
                bottom=asset_up.Open,
                fill_color="#00D09C", # A nice green
                line_color="black"
                )
            stocksFigure.vbar(
                x=asset_down.index,
                width=bar_width_ms,
                top=asset_down.Open,   # Note: top is open and bottom is close for down days
                bottom=asset_down.Close,
                fill_color="#F25865", # A nice red
                line_color="black"
                )
        

        capitalFigure = figure(
        height = height,
        width = width,
        x_axis_type="datetime",
        title="Capital Over Time",
        x_range=stocksFigure.x_range 
        )
        capitalFigure.line(
            x= self.capitalOverTime.index,
            y=self.capitalOverTime['Capital'],
            legend_label="Capital",
            color="black",
            line_width=2
        )
        capitalFigure.legend.location = "top_left"

        layout = column(stocksFigure, capitalFigure)

        show( layout)