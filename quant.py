import numpy as np
import QuantLib as ql

def binomial_model(S0: float, K: float, r: float, T: float, sigma: float, N: int, option_type: str) -> float:
    """
    Price an option using the Binomial Option Pricing Model via QuantLib.
    
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
    
    Returns:
    -------
    float
        The calculated price of the option.
    """
    # Option Type
    if option_type.lower() == 'call':
        option_type_ql = ql.Option.Call
    elif option_type.lower() == 'put':
        option_type_ql = ql.Option.Put
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    # Option Details
    payoff = ql.PlainVanillaPayoff(option_type_ql, K)
    exercise = ql.AmericanExercise(ql.Date.todaysDate(), ql.Date.todaysDate() + int(T * 365))
    
    # Create the option
    option = ql.VanillaOption(payoff, exercise)

    # Market Data
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(S0))
    risk_free_curve = ql.YieldTermStructureHandle(ql.FlatForward(0, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(r)), ql.Actual360()))
    volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(0, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(sigma)), ql.Actual360()))

    # Black-Scholes Process
    process = ql.BlackScholesProcess(spot_handle, risk_free_curve, volatility)

    # Pricing Engine
    engine = ql.BinomialVanillaEngine(process, "crr", N)
    option.setPricingEngine(engine)

    # Return the price
    return option.NPV()

def get_greeks(S0, K, r, T, sigma, N, option_type='call'):
    """
    Calculate the Delta, Gamma, Theta, and Vega of an option using the Binomial Option Pricing Model.
    
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
    
    Returns:
    -------
    tuple
        A tuple containing the calculated Delta, Gamma, Theta, and Vega.
    """
    
    # Small perturbations for numerical differentiation
    dS = 0.05 * S0  # Larger change in stock price
    dT = 1e-3 * T   # Larger change in time to maturity
    dsigma = 0.05 * sigma  # Larger change in volatility

    # Option price at the current stock price
    price_current = binomial_model(S0, K, r, T, sigma, N, option_type)

    # Delta: Change in option price with respect to a change in stock price
    price_up = binomial_model(S0 + dS, K, r, T, sigma, N, option_type)
    price_down = binomial_model(S0 - dS, K, r, T, sigma, N, option_type)
    delta = (price_up - price_down) / (2 * dS)

    # Gamma: Change in Delta with respect to a change in stock price
    delta_up = (binomial_model(S0 + dS, K, r, T, sigma, N, option_type) - binomial_model(S0, K, r, T, sigma, N, option_type)) / dS
    delta_down = (binomial_model(S0, K, r, T, sigma, N, option_type) - binomial_model(S0 - dS, K, r, T, sigma, N, option_type)) / dS
    gamma = (delta_up - delta_down) / (2 * dS)

    # Theta: Change in option price with respect to time to maturity
    price_time_up = binomial_model(S0, K, r, T - dT, sigma, N, option_type)
    theta = (price_time_up - price_current) / dT

    # Vega: Change in option price with respect to volatility
    price_vol_up = binomial_model(S0, K, r, T, sigma + dsigma, N, option_type)
    vega = (price_vol_up - price_current) / dsigma

    return delta, gamma, theta, vega

def option_payoff(option_type, S, K, premium, contract_fee=0):
    """
    Calculate the payoff for a single option at expiration, accounting for contract fee.
    
    Parameters:
    ----------
    option_type : str
        Type of the option ('call' or 'put').
    S : float
        Spot price at expiration.
    K : float
        Strike price.
    premium : float
        Premium paid (for long options) or received (for short options).
    contract_fee : float
        Transaction fee for each option contract (optional).
    
    Returns:
    -------
    float
        The payoff of the option.
    """
    if option_type.lower() == 'call':
        payoff = max(0, S - K)
    elif option_type.lower() == 'put':
        payoff = max(0, K - S)
    else:
        raise ValueError("Option type must be 'call' or 'put'.")
    
    # Deduct the contract fee from the payoff (if any)
    return payoff - contract_fee

def strategy_pnL(underlying_prices, strategy):
    """
    Calculate the PnL for a strategy, which can include multiple options.
    
    Parameters:
    ----------
    underlying_prices : list
        List of possible spot prices at expiration.
    strategy : list
        List of tuples specifying the strategy. Each tuple should contain:
        - ('option_type', strike_price, premium_paid/received, time_to_expiry, contract_fee).
    
    Returns:
    -------
    np.array
        Array of PnL values for each underlying price.
    """
    pnl = np.zeros(len(underlying_prices))  # Initialize an array to hold the PnL for each price
    
    for option_type, strike, premium, T, contract_fee in strategy:
        for i, S in enumerate(underlying_prices):
            # Calculate the option payoff, including the contract fee
            pnl[i] += option_payoff(option_type, S, strike, premium, contract_fee)
    
    return pnl
