import warnings

import QuantLib as ql
from .option import Option

TRADING_DAYS = 252

class OptionPricer:
    @staticmethod
    def binomial_model(option: Option, risk_free_rate: int, N: int = 1000) -> float:
        """Price an option using the Binomial Option Pricing Model.
        
        Args:
            option (Option): Option object.
            risk_free_rate (int): Risk-free rate. (Annualized)
            N (int): Number of time steps.
            
        Returns:
            float: Option price.
        """
        
        option_type = option.option_type
        K = option.strike
        S0 = option.underlying_price
        T = option.time_to_expiry / TRADING_DAYS
        r = risk_free_rate
        sigma = option.sigma
        is_american = option.is_american
        
        if option_type.lower() == 'call':
            option_type_ql = ql.Option.Call
        elif option_type.lower() == 'put':
            option_type_ql = ql.Option.Put
        else:
            raise ValueError("option_type must be 'call' or 'put'.")

        today = ql.Date.todaysDate()
        maturity_date = today + int(T * 365)
        ql.Settings.instance().evaluationDate = today

        payoff = ql.PlainVanillaPayoff(option_type_ql, K)
        exercise = ql.AmericanExercise(today, maturity_date) if is_american else ql.EuropeanExercise(maturity_date)

        option = ql.VanillaOption(payoff, exercise)

        spot_handle = ql.QuoteHandle(ql.SimpleQuote(S0))
        risk_free_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(r)), ql.Actual360()))
        volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(sigma)), ql.Actual360()))

        process = ql.BlackScholesProcess(spot_handle, risk_free_curve, volatility)
        engine = ql.BinomialVanillaEngine(process, "crr", N)
        option.setPricingEngine(engine)

        return option.NPV()
    
    @staticmethod
    def black_scholes_merton(option: Option, risk_free_rate: int) -> float:
        """Price an option using the Black-Scholes-Merton Model.
        
        Args:
            option (Option): Option object.
            risk_free_rate (int): Risk-free rate. (Annualized)
            
        Returns:
            float: Option price.
        """

        if option.is_american:
            warnings.warn("Black-Scholes-Merton model does not support American options. Using a European option.", category=UserWarning)

        option_type = option.option_type
        K = option.strike
        S0 = option.underlying_price
        T = option.time_to_expiry / TRADING_DAYS
        r = risk_free_rate
        sigma = option.sigma

        if option_type.lower() == 'call':
            option_type_ql = ql.Option.Call
        elif option_type.lower() == 'put':
            option_type_ql = ql.Option.Put
        else:
            raise ValueError("option_type must be 'call' or 'put'.")

        today = ql.Date.todaysDate()
        maturity_date = today + int(T * 365)
        ql.Settings.instance().evaluationDate = today

        payoff = ql.PlainVanillaPayoff(option_type_ql, K)
        exercise = ql.EuropeanExercise(maturity_date)

        option_ql = ql.VanillaOption(payoff, exercise)

        spot_handle = ql.QuoteHandle(ql.SimpleQuote(S0))
        risk_free_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(r)), ql.Actual360()))
        volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(sigma)), ql.Actual360()))

        process = ql.BlackScholesProcess(spot_handle, risk_free_curve, volatility)
        engine = ql.AnalyticEuropeanEngine(process)
        option_ql.setPricingEngine(engine)

        return option_ql.NPV()

