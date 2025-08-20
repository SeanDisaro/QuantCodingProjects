# QuantCodingProjects
Some Coding Projects to Explore some Quant Finance Methods.
We use python 3.13

These are just some fun coding projects which I do as a preparation to being a Quant.

![Alt Text](./animations/probPriceUnder.gif)

## BlackScholesMonteCarloEuropoeanOptionPricing.ipynb
This is a notebook, where we do some **Monte Carlo Black Scholes optoion pricing**. We also use a **variance reduction method** for our monte carlo simulation, to improve the results, when we want to predict exotic europeans!

## TeslaOptionPriceGARCH.ipynb

In this notebook, we **predict the volatility** of the Tesla stock in advance using a **GARCH** model and then compare, if this gives us an edge in option pricing when using the Black Scholes formula with just the **historic volatility** at the current day.
This is then used to build a **delta hedged** portfolio.
## pe_500s&p_by_sector_industry.ipynb

This notebook scrapes all the S&P500 symbols from wikipedia, then gets the pe ratios and industries from yahoo finance and then checks which companies have a pe ratio which is well below (1 std deviation) under the industries mean pe ratio.