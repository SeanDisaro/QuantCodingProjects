import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def deltaEuropean_BS(r: float, t:float, T:float, K:float, S:float, sigma: float, option_type='call'):
    """returns delta for european option under Black Scholes.

    Args:
        r (float): risk free rate
        t (float): initial time
        T (float): maturity
        K (float): Strike
        S (float): Stock Price
        sigma (float): volatility
        option_type (str): Type of the option, 'call' or 'put'.

    Returns:
        (float): delta under Black Scholes for a european option
    """
    d1 = (np.log(S / K) + (r  + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    if option_type == "call":
        return np.exp( T) * stats.norm.cdf(d1)
    elif option_type == "put":
        return -np.exp( T) * stats.norm.cdf(-d1)


def black_scholes_gamma(S:float, K:float, T:float, r:float, sigma:float):
    """
    Calculates the Gamma of a European option using the Black-Scholes model.

    Gamma measures the rate of change of an option's delta with respect to a change
    in the underlying asset's price. It indicates how sensitive the delta is
    to movements in the underlying price.

    Args:
        S (float): Current price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to expiration (in years).
        r (float): Risk-free interest rate (annualized, continuously compounded).
        sigma (float): Volatility of the underlying asset's returns (annualized).

    Returns:
        (float): The Gamma of the option.
    """

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    N_prime_d1 = stats.norm.pdf(d1)
    gamma = N_prime_d1 / (S * sigma * np.sqrt(T))

    return gamma


def american_put_delta_binomial(r: float,  T:float, K:float, S0:float, sigma: float, n:int):
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
    stock_prices = np.zeros((n + 1, n + 1))
    stock_prices[0, 0] = S0
    for i in range(1, n + 1):
        stock_prices[i, 0] = stock_prices[i - 1, 0] * d
        for j in range(1, i + 1):
            stock_prices[i, j] = stock_prices[i - 1, j - 1] * u

    option_values = np.maximum(0, K - stock_prices[n, :])

    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            continuation_value = np.exp(-r * dt) * (p * option_values[j + 1] + (1 - p) * option_values[j])
            exercise_value = max(0, K - stock_prices[i, j])
            option_values[j] = max(continuation_value, exercise_value)

    delta = (option_values[1] - option_values[0]) / (stock_prices[1, 1] - stock_prices[1, 0])
    
    return delta




import numpy as np

def american_put_gamma_binomial(S0:float, K:float, T:float, r:float, sigma:float, N:int):
    """
    Computes the Gamma of an American put option using the Binomial Tree Model.

    Args:
        S0 (float): Current stock price.
        K (float): Strike price.
        T (float): Time to maturity (in years).
        r (float): Risk-free interest rate (annualized).
        sigma (float): Volatility of the underlying asset (annualized).
        N (int): Number of steps in the binomial tree.
                 Must be at least 2 for Gamma calculation.

    Returns:
        (float): The Gamma of the American put option.
    """


    dt = T / N  
    u = np.exp(sigma * np.sqrt(dt)) 
    d = 1 / u 
    p = (np.exp(r * dt) - d) / (u - d) 

    stock_prices = np.zeros((N + 1, N + 1))
    option_values = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        for j in range(i + 1):
            stock_prices[i, j] = S0 * (u ** j) * (d ** (i - j))

    option_values[N, :] = np.maximum(0, K - stock_prices[N, :])


    for i in range(N - 1, -1, -1): 
        for j in range(i + 1): 
            continuation_value = np.exp(-r * dt) * (p * option_values[i + 1, j + 1] + (1 - p) * option_values[i + 1, j])

            exercise_value = max(0, K - stock_prices[i, j])
            

            option_values[i, j] = max(continuation_value, exercise_value)



    S_up = stock_prices[1, 1]  
    S_down = stock_prices[1, 0]


    S_up_up = stock_prices[2, 2]    
    S_up_down = stock_prices[2, 1]   
    S_down_down = stock_prices[2, 0]


    V_up_up = option_values[2, 2]     
    V_up_down = option_values[2, 1]    
    V_down_down = option_values[2, 0]  


    delta_up = (V_up_up - V_up_down) / (S_up_up - S_up_down)

    delta_down = (V_up_down - V_down_down) / (S_up_down - S_down_down)

    gamma = (delta_up - delta_down) / (S_up - S_down)

    return gamma
