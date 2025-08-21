# QuantCodingProjects
Some Coding Projects to Explore some Quant Finance Methods.
We use python 3.13

These are just some fun coding projects which I do as a preparation to being a Quant.

![Alt Text](./animations/probPriceUnder.gif)
**This Animation gets updated after every trading day**

If you want to understand how this animation was created, then you can check out the `plotProbabilitesNvidia_UpDown.ipynb` notebook.

## Nvidia sentiment analysis (Automatically updated after every trading day)
![image](./pictures/ratingPlot.png)

![image](./pictures/textRating.png)

## Daily Updated Bullet Points for Sentiment Analysis for NVIDIA stock
<!-- BulletPointStart -->
- Wedbush analyst Dan Ives says the market dip is short-term and presents an opportunity to own the AI-driven core winners; Nvidia is expected to remain central to the AI revolution with roughly a 10:1 demand-to-supply ratio for its chips.  
- Nvidia has fallen about 3% this week amid a broader tech sell-off, but the “1996 moment” analogy and AI rally thesis suggest the upcycle could continue for several years.  
- TipRanks shows Nvidia among stocks with Strong Buy ratings; among peers in the group, Micron (MU) carries the highest upside potential at about 31% to a $153.81 target.  
- Regulators in China are moving to restrict Nvidia’s China-specific H20 AI processor sales, following remarks by U.S. officials, signaling potential regulatory headwinds for Nvidia in China.  
- UBS’s Timothy Arcuri maintains a Buy with a $205 target; Oppenheimer reiterates Buy with a $200 target; Nvidia’s latest quarterly revenue was $44.06B with net profit of $18.78B, while insider selling has been notable (e.g., Mark A. Stevens sold 608,248 shares for ~$88.35M).  


<!-- BulletPointEnd -->
These Bullet Points get updated after every trading day
## plotProbabilitesNvidia_UpDown.ipynb

This notebook explains how to translate **option prices to probabilities** on where the price of a stock will be at future times. This is used to derive **probability density functions** which illustrate how likeley it is that a stock will be under/above some price at some time. See the animatino above or the following heatmap:
![image](./pictures/probPriceUnder.png)

## TeslaOptionPriceGARCH.ipynb

In this notebook, we **predict the volatility** of the Tesla stock in advance using a **GARCH** model trained with the **historic volatility**. This is then used to price options with Black Scholes and the Binomial tree model. We compare the values we get with the **market values** and the **implied volatility** of said options. The actual prices we predicted differ from the market prices. We assume that our prediction gives us an edge (not really but just for the sake of coding and having a little bit of fun) and we construct a Delta and Gamma Hedged portfolio with calls, puts and the underlying tesla stock.
This is then used to build a **delta hedged** portfolio.



## pe_500s&p_by_sector_industry.ipynb

This notebook **scrapes** all the **S&P500 symbols from wikipedia**, then gets the **pe ratios and industries** from yahoo finance and then checks which companies have a pe ratio which is well below (1 std deviation) under the industries mean pe ratio. This is a very basic screening which might be interesting to fundamentalists.



## BlackScholesMonteCarloEuropoeanOptionPricing.ipynb
This is a notebook, where we do some **Monte Carlo Black Scholes optoion pricing**. We also use a **variance reduction method** for our monte carlo simulation, to improve the results, when we want to predict exotic europeans!

