import numpy as np
from scipy import stats
import matplotlib.pyplot as plt




def analyticEuropeanCall_BS(r: float, t:float, T:float, K:float, S:float, sigma: float):
    """returns analytic price for european call option under Black Scholes

    Args:
        r (float): risk free rate
        t (float): initial time
        T (float): maturity
        K (float): Strike
        S (float): Stock Price
        sigma (float): volatility

    Returns:
        (float): Analytic price under Black Scholes for a european call option
    """
    d1 = (np.log(S/K) + (r + sigma**2 /2)* (T-t))/ (sigma * np.sqrt(T-t))
    d2 = d1 - sigma* np.sqrt(T-t)
    return (S* stats.norm.cdf(d1) - K *np.exp(-r*(T-t))*stats.norm.cdf(d2)).item()




def analyticEuropeanPut_BS(r: float, t:float, T:float, K:float, S:float, sigma: float):
    """returns analytic price for european put option under Black Scholes

    Args:
        r (float): risk free rate
        t (float): initial time
        T (float): maturity
        K (float): Strike
        S (float): Stock Price
        sigma (float): volatility

    Returns:
        (float): Analytic price under Black Scholes for a european put option
    """
    d1 = (np.log(S/K) + (r + sigma**2 /2)* (T-t))/ (sigma * np.sqrt(T-t))
    d2 = d1 - sigma* np.sqrt(T-t)
    return (-S* stats.norm.cdf(-d1) + K *np.exp(-r*(T-t))*stats.norm.cdf(-d2)).item()









def price_american_option_binomial(S:float, K:float, T:float, r:float, sigma:float, n:int, option_type='call'):
    """
    Prices an American option using the Cox-Ross-Rubinstein binomial tree model.

    Args:
        S (float): Current stock price.
        K (float): Strike price of the option.
        T (float): Time to expiration in years.
        r (float): Risk-free interest rate (annual).
        sigma (float): Volatility of the underlying stock (annual).
        n (int): Number of steps in the binomial tree.
        option_type (str): Type of the option, 'call' or 'put'.

    Returns:
        (float): The estimated price of the American option.
    """

    dt = T / n
    

    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    

    p = (np.exp(r * dt) - d) / (u - d)

    discount = np.exp(-r * dt)

    asset_prices = np.zeros(n + 1)
    for i in range(n + 1):
        asset_prices[i] = S * (u**(n - i)) * (d**i)


    option_values = np.zeros(n + 1)
    if option_type == 'call':
        option_values[:] = np.maximum(0, asset_prices - K)
    else: 
        option_values[:] = np.maximum(0, K - asset_prices)

    for i in range(n - 1, -1, -1):

        for j in range(i + 1):

            continuation_value = discount * (p * option_values[j] + (1 - p) * option_values[j + 1])

            current_asset_price = S * (u**(i - j)) * (d**j)
  
            if option_type == 'call':
                exercise_value = np.maximum(0, current_asset_price - K)
            else: 
                exercise_value = np.maximum(0, K - current_asset_price)

            option_values[j] = np.maximum(continuation_value, exercise_value)

    return option_values[0]