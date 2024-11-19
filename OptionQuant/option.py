import numpy as np

class Option:
    def __init__(self,
                 option_type: str,
                 underlying_price: float,
                 strike: float,
                 premium: float,
                 time_to_expiry: float,
                 sigma: float, 
                 contract_fee: float,
                 is_american: bool = True):
        self.option_type = option_type
        self.underlying_price = underlying_price
        self.strike = strike
        self.premium = premium
        self.time_to_expiry = time_to_expiry
        self.sigma = sigma
        self.contract_fee = contract_fee
        self.is_american = is_american

        self.lst_underlying_prices = np.linspace(0.8 * self.strike, 1.2 * self.strike, 1000)

    def pnl(self,
            underlying_prices: np.ndarray = []) -> np.ndarray:
        """Calculate the PnL for this option across a range of underlying prices.

        Args:
            underlying_prices (np.ndarray): Array of underlying prices, default is 20% below and 20% above the strike price.

        Returns:
            np.ndarray: Array of PnL values.
        """

        if not len(underlying_prices) == 0:
            underlying_prices = self.lst_underlying_prices

        if self.option_type.lower() == 'call':
            payoff = np.maximum(0, underlying_prices - self.strike)
        elif self.option_type.lower() == 'put':
            payoff = np.maximum(0, self.strike - underlying_prices)
        else:
            raise ValueError("Option type must be 'call' or 'put'.")

        if self.premium > 0:  # Long position
            pnl = payoff - self.premium - self.contract_fee
        else:  # Short position
            pnl = payoff + abs(self.premium) - self.contract_fee

        return pnl