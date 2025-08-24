import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.dates import date2num, DateFormatter
from datetime import datetime
from matplotlib.animation import FuncAnimation, PillowWriter
import yfinance as yf
from src.PricingFunctions import *




def plotCDFStockPrices():

    # Probabilities directly from stock prices
    ticker = yf.Ticker("NVDA")
    expiry_dates = ticker.options

    possibleStrikes = set(ticker.option_chain(expiry_dates[0]).calls["strike"])


    for i in range(len(expiry_dates)):
        strikes_Call = set(ticker.option_chain(expiry_dates[i]).calls["strike"])
        strikes_Put = set(ticker.option_chain(expiry_dates[i]).puts["strike"])
        possibleStrikes = possibleStrikes.intersection(strikes_Call)
        possibleStrikes = possibleStrikes.intersection(strikes_Put)

    possibleStrikes = sorted(list(possibleStrikes))


    cdf_how_likeley_Stock_Under_Strike = np.zeros((len(expiry_dates), len(possibleStrikes)))
    for i in range(len(expiry_dates)):
        callsForThisExpiry = ticker.option_chain(expiry_dates[i]).calls
        putsForThisExpiry = ticker.option_chain(expiry_dates[i]).puts
        for j in range(len(possibleStrikes)):
            callsPrice =  callsForThisExpiry[callsForThisExpiry['strike'] == possibleStrikes[j]]["lastPrice"].item()
            putPrice =  putsForThisExpiry[putsForThisExpiry['strike'] == possibleStrikes[j]]["lastPrice"].item()
            cdf_how_likeley_Stock_Under_Strike[i,j] = putPrice/(putPrice +callsPrice)






    x_dates = np.array([datetime.strptime(d, "%Y-%m-%d") for d in expiry_dates])
    x_num = date2num(x_dates)
    X, Y = np.meshgrid(x_num, possibleStrikes, indexing="ij")  # shape (N,M)


    # Plot setup
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(X, Y, cdf_how_likeley_Stock_Under_Strike, cmap=cm.viridis, edgecolor="none")

    ax.set_title("Cumulative Distribution Function Nvidia Stock over Time (From Option Prices)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")
    ax.set_zlabel("Probability")
    ax.xaxis_date()
    fig.autofmt_xdate()

    # Animation function (rotate around azimuth angle)
    def rotate(angle):
        ax.view_init(elev=30, azim=angle)

    # Make animation
    anim = FuncAnimation(fig, rotate, frames=np.arange(0, 360, 2), interval=100)


    anim.save("./animations/probPriceUnder.gif", writer=PillowWriter(fps=10))




    fig, ax = plt.subplots(figsize=(10, 6))

    c = ax.pcolormesh(X, Y, cdf_how_likeley_Stock_Under_Strike, cmap="viridis", shading="auto")

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()

    ax.set_title("Probability that NVIDIA price will be under some value at some time (From Option Prices)")
    ax.set_xlabel("Date")
    ax.set_ylabel("StockPrice")
    plt.colorbar(c, ax=ax, label="Probability")

    plt.savefig("./pictures/probPriceUnder.png")

    # Probabilities with Breeden Litzenberg via mean implied volatility
    plt.clf()

    IVs = []
    for i in range(len(expiry_dates)):
        calls = ticker.option_chain(expiry_dates[i]).calls
        puts = ticker.option_chain(expiry_dates[i]).puts
        calls_IVs = calls["impliedVolatility"].to_list()
        puts_IVs = puts["impliedVolatility"].to_list()
        IVs = IVs + calls_IVs + puts_IVs

    iv_mean = np.mean(IVs)

    S0 = ticker.history(period="1d")['Close'].iloc[-1]
    r = 0.0426  
    sigma = iv_mean 

    minK = min(possibleStrikes)
    maxK = max(possibleStrikes)

    # for finite differences
    N = 1000
    pdf_breedenLitzenberg = np.zeros((len(expiry_dates), N))
    h = (maxK - minK) / N


    for i in range(len(expiry_dates)):
        daysLeft = (datetime.strptime(expiry_dates[i], "%Y-%m-%d").date() - datetime.now().date()).days
        T = daysLeft /365
        c_Minus = analyticEuropeanCall_BS(r, 0, T, minK - h, S0, sigma)
        c_At = analyticEuropeanCall_BS(r, 0, T, minK , S0, sigma)
        c_Plus = analyticEuropeanCall_BS(r, 0, T, minK + h, S0, sigma)
        for k in range(N):
            pdf_breedenLitzenberg[i, k] = (c_Plus - 2*c_At + c_Minus) / (h**2)
            c_Minus = c_At
            c_At = c_Plus
            c_Plus = analyticEuropeanCall_BS(r, 0, T, minK + h*(k+2), S0, sigma)
        
        pdf_breedenLitzenberg[i, :] = pdf_breedenLitzenberg[i, :] * np.exp(r*T)

    cdf_Put_BreedenLitzenberg = np.zeros_like(pdf_breedenLitzenberg)

    for i in range(len(expiry_dates)):
        sumDensities = 0
        for k in range(N):
            sumDensities += pdf_breedenLitzenberg[i,k]
            cdf_Put_BreedenLitzenberg[i,k] = sumDensities * h

    k_Ax = np.arange(minK, maxK, h)

    plt.clf()

    x_num = date2num(x_dates)
    X, Y = np.meshgrid(x_num, k_Ax, indexing="ij")  # shape (N,M)


    # Plot setup
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(X, Y, cdf_Put_BreedenLitzenberg, cmap=cm.viridis, edgecolor="none")

    ax.set_title("Cumulative Distribution Function Nvidia Stock over Time (Via Breeden Litzenberg)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")
    ax.set_zlabel("Probability")
    ax.xaxis_date()
    fig.autofmt_xdate()

    # Animation function (rotate around azimuth angle)
    def rotate(angle):
        ax.view_init(elev=30, azim=angle)

    # Make animation
    anim = FuncAnimation(fig, rotate, frames=np.arange(0, 360, 2), interval=100)


    anim.save("./animations/probPriceUnderBreedenLitzenberg.gif", writer=PillowWriter(fps=10))


    fig, ax = plt.subplots(figsize=(10, 6))

    c = ax.pcolormesh(X, Y, cdf_Put_BreedenLitzenberg, cmap="viridis", shading="auto")

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()

    ax.set_title("Probability that NVIDIA price will be under some value at some time (Breeden Litzenberg)")
    ax.set_xlabel("Date")
    ax.set_ylabel("StockPrice")
    plt.colorbar(c, ax=ax, label="Probability")

    plt.savefig("./pictures/probPriceUnderBreedenLitzenberg.png")