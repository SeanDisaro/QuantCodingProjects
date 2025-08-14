import numpy as np
from scipy import stats
import matplotlib.pyplot as plt




def analyticEuropeanCall(r: float, t:float, T:float, K:float, S:float, sigma: float):
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




def analyticEuropeanPut(r: float, t:float, T:float, K:float, S:float, sigma: float):
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