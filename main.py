import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.dates import date2num, DateFormatter
import datetime
from matplotlib.animation import FuncAnimation, PillowWriter
import yfinance as yf





ticker = yf.Ticker("NVDA")
expiry_dates = ticker.options

possibleStrikes = set(ticker.option_chain(expiry_dates[0]).calls["strike"])


for i in range(len(expiry_dates)):
    strikes_Call = set(ticker.option_chain(expiry_dates[i]).calls["strike"])
    strikes_Put = set(ticker.option_chain(expiry_dates[i]).puts["strike"])
    possibleStrikes = possibleStrikes.intersection(strikes_Call)
    possibleStrikes = possibleStrikes.intersection(strikes_Put)

possibleStrikes = sorted(list(possibleStrikes))


pdf_how_likeley_Stock_Under_Strike = np.zeros((len(expiry_dates), len(possibleStrikes)))
for i in range(len(expiry_dates)):
    callsForThisExpiry = ticker.option_chain(expiry_dates[i]).calls
    putsForThisExpiry = ticker.option_chain(expiry_dates[i]).puts
    for j in range(len(possibleStrikes)):
        callsPrice =  callsForThisExpiry[callsForThisExpiry['strike'] == possibleStrikes[j]]["lastPrice"].item()
        putPrice =  putsForThisExpiry[putsForThisExpiry['strike'] == possibleStrikes[j]]["lastPrice"].item()
        pdf_how_likeley_Stock_Under_Strike[i,j] = putPrice/(putPrice +callsPrice)






x_dates = np.array([datetime.datetime.strptime(d, "%Y-%m-%d") for d in expiry_dates])
x_num = date2num(x_dates)
X, Y = np.meshgrid(x_num, possibleStrikes, indexing="ij")  # shape (N,M)


# Plot setup
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

surf = ax.plot_surface(X, Y, pdf_how_likeley_Stock_Under_Strike, cmap=cm.viridis, edgecolor="none")

ax.set_title("Probability that NVIDIA price will be under some value at some time")
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

c = ax.pcolormesh(X, Y, pdf_how_likeley_Stock_Under_Strike, cmap="viridis", shading="auto")

ax.xaxis_date()
ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()

ax.set_title("Probability that NVIDIA price will be under some value at some time")
ax.set_xlabel("Date")
ax.set_ylabel("StockPrice")
plt.colorbar(c, ax=ax, label="Probability")

plt.savefig("./pictures/probPriceUnder.png")