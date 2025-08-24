# QuantCodingProjects
Some Coding Projects to Explore some Quant Finance Methods.
We use python 3.13

These are just some fun coding projects which I do as a preparation to being a Quant.


![Alt Text](./animations/probPriceUnder.gif)
![Alt Text](./animations/probPriceUnderBreedenLitzenberg.gif)
**These Animations get updated after every trading day**

If you want to understand how this animation was created, then you can check out the `plotProbabilitesNvidia_UpDown.ipynb` notebook.

## Nvidia sentiment analysis (Automatically updated after every trading day with GitHub Actions)
![image](./pictures/ratingPlot.png)

<!--![image](./pictures/textRating.png)-->

# Daily Updated Bullet Points for Sentiment Analysis for NVIDIA stock
<!-- BulletPointStart -->
- Nvidia halted H20 AI chip production for China over security concerns and is pursuing a modified Blackwell design (lower power, ~80% of top performance) to try to win regulatory approval; China remains a key market with potential Chinese AI-chip spend estimated by analysts at over $15B, while a 15% of H20 revenue would need to go to the US Treasury if licenses are granted.

- The stock remains very buoyant on Wall Street, with a Strong Buy consensus across analysts (roughly 35+ buys vs. a few holds/sells); average price targets are in the high-$190s to low-$200s, implying about 11%–12% upside (some reports note up to ~14%).

- Ahead of the Q2 FY26 results, analysts expect roughly $1.01 EPS on about $45.9B in revenue; demand from AI/data-center workloads is strong, though China-related sales may be excluded from guidance pending license clearances.

- Valuation remains rich but supported by growth: forward P/E around the low- to mid-30s (with some commentary noting it’s high but justified by rapid earnings growth), and targets imply modest single-digit to low-double-digit upside relative to current levels.

- Near-term catalysts include the rollout of next-generation GPUs (Blackwell/Ultra, GB300) and continued AI demand momentum; supply is largely sold out for the coming year, which underpins growth but adds sensitivity to regulatory and China-related developments.

Market optimism rating: 
<!-- BulletPointEnd -->

These Bullet Points get updated after every trading day. They are based on news articles from [News Articles about Nvidia](https://markets.businessinsider.com/news/nvda-stock). They get summarized by ChatGPT into the bullet points above and on top of that ChatGPT gives an optimism ranking from 1-10 for the Nvidia stock based on the articles, which is displayed above.
## plotProbabilitesNvidia_UpDown.ipynb

This notebook explains how to translate **option prices to probabilities** on where the price of a stock will be at future times.
We explore **two possibilities to derive these probabilities**. One directly from the option prices and one via the **Breeden Litzenberg formula**
This is used to derive **probability density functions** which illustrate how likeley it is that a stock will be under/above some price at some time. See the animations above or compare the following heatmaps:
![image](./pictures/probPriceUnder.png)
![image](./pictures/probPriceUnderBreedenLitzenberg.png)
(These get updated daily)

## pairsTradingAndIndustryTrading.ipynb
![image](./pictures/pairsTradingPic.png)
1) In this notebook we search for correlated stocks in the S&P500. Since we do not want to compute a 500x500 **correlation matrix**, we instead only search for correlated **S&P500 stocks within each industry**. After we find a pair, we find the right scaling factor, to bring the stock prices to the same level (via a **linear regression model without intercept**). After that, we conduct an **Augmented Dickey–Fuller test**, to see if the increments of the two time serieses are in fact **stationary**. Then, we implement a simple **pairs trading strategy** within the backtesting framework, which I have implemented (see `src/backtesting`).

## Backtesting framework
I implemented a simple backtesting framework. The reason for this is that I was not happy with the python packages I found for backtesting strategies, since they either only work for single asset strategies or they are only supported by older python versions. To see the source code for this, check out `src/backtesting`. There you have a class `Backtester`, which implements (multiple asset) data feeding (via pandas DataFrames), ploting, reporting results and of course the actual backtesting engine. You will also find a class `Strategy`, which is mean to be a parent class which you can inherit to build your own trading strategy.

## TeslaOptionPriceGARCH.ipynb

In this notebook, we **predict the volatility** of the Tesla stock in advance using a **GARCH** model trained with the **historic volatility**. This is then used to price options with Black Scholes and the Binomial tree model. We compare the values we get with the **market values** and the **implied volatility** of said options. The actual prices we predicted differ from the market prices. We assume that our prediction gives us an edge (not really but just for the sake of coding and having a little bit of fun) and we construct a Delta and Gamma Hedged portfolio with calls, puts and the underlying tesla stock.
This is then used to build a **delta hedged** portfolio.



## pe_500s&p_by_sector_industry.ipynb

This notebook **scrapes** all the **S&P500 symbols from wikipedia**, then gets the **pe ratios and industries** from yahoo finance and then checks which companies have a pe ratio which is well below (1 std deviation) under the industries mean pe ratio. This is a very basic screening which might be interesting to fundamentalists.



## BlackScholesMonteCarloEuropoeanOptionPricing.ipynb
This is a notebook, where we do some **Monte Carlo Black Scholes optoion pricing**. We also use a **variance reduction method** for our monte carlo simulation, to improve the results, when we want to predict exotic europeans!

