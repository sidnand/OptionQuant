import matplotlib.pyplot as plt
import numpy as np

from quant import *

def plot_greeks_vs_underlying(S0, K, r, T, sigma, N, option_type='call'):
    """
    Plot the Delta, Gamma, Theta, and Vega of an option as functions of the underlying price.
    
    Parameters:
    ----------
    S0 : float
        Initial stock price.
    K : float
        Strike price of the option.
    r : float
        Risk-free interest rate (annualized, continuous compounding).
    T : float
        Time to maturity (in years).
    sigma : float
        Volatility of the underlying stock (annualized).
    N : int
        Number of time steps in the binomial tree.
    option_type : str
        Type of option to price: 'call' or 'put'.
    """

    # Create a range of underlying asset prices around S0
    S0_range = np.linspace(S0 * 0.5, S0 * 1.5, 100)  # 50% to 150% of current price
    
    # Initialize lists to store the Greek values
    delta_vals = []
    gamma_vals = []
    theta_vals = []
    vega_vals = []
    
    # Calculate Greeks for each price in the range
    for price in S0_range:
        delta, gamma, theta, vega = get_greeks(price, K, r, T, sigma, N, option_type)
        delta_vals.append(delta)
        gamma_vals.append(gamma)
        theta_vals.append(theta)
        vega_vals.append(vega)
    
    # Plot the Greeks
    plt.figure(figsize=(10, 6))
    
    # Plot Delta
    plt.subplot(2, 2, 1)
    plt.plot(S0_range, delta_vals, label='Delta', color='blue')
    plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
    plt.title('Delta vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Delta')
    
    # Plot Gamma
    plt.subplot(2, 2, 2)
    plt.plot(S0_range, gamma_vals, label='Gamma', color='green')
    plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
    plt.title('Gamma vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Gamma')
    
    # Plot Theta
    plt.subplot(2, 2, 3)
    plt.plot(S0_range, theta_vals, label='Theta', color='red')
    plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
    plt.title('Theta vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Theta')
    
    # Plot Vega
    plt.subplot(2, 2, 4)
    plt.plot(S0_range, vega_vals, label='Vega', color='orange')
    plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
    plt.title('Vega vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Vega')

    plt.tight_layout()

def plot_pnL(strategy, S0, price_range=None):
    """
    Plot the PnL of the given strategy, including time to expiry and contract fee.
    
    Parameters:
    ----------
    strategy : list
        List of tuples specifying the strategy. Each tuple should contain:
        - ('option_type', strike_price, premium_paid/received, time_to_expiry, contract_fee).
    S0 : float, optional
        Current price of the underlying asset.
    price_range : tuple, optional
        Range of prices to simulate the PnL. Default is None, which will create a range based on S0.
    """

    if price_range is None:
        price_range = (S0 * 0.95, S0 * 1.05)  # Default range, 10% above and below the current price
        
    # Generate a range of possible prices at expiration
    underlying_prices = np.linspace(price_range[0], price_range[1], 600)

    # Calculate PnL
    pnl = strategy_pnL(underlying_prices, strategy)

    # Plot the PnL curve
    plt.figure(figsize=(10, 6))
    plt.plot(underlying_prices, pnl, label='Strategy PnL')
    plt.axhline(0, color='black', lw=1, label='Breakeven')
    plt.axvline(S0, color='gray', linestyle='--', label='Current Price')
    plt.title('PnL of the Option Strategy')
    plt.xlabel('Underlying Price at Expiration')
    plt.ylabel('Profit and Loss')
    plt.legend()
    plt.grid(True)