import numpy as np
import matplotlib.pyplot as plt

from .option import Option

class OptionStrategy:
    def __init__(self, options: list[Option], underlying_prices: np.ndarray):
        """Initialize OptionStrategy object.

        Args:
            options (list[Option]): List of Option objects.
            underlying_prices (np.ndarray): Array of underlying prices.
        """

        if underlying_prices is None or len(underlying_prices) == 0:
            raise ValueError("Underlying prices must be provided at initialization.")

        self.options = options
        self.underlying_prices = underlying_prices
        self.strategy_pnl_values = self._pnl()
        self.break_even_underlying = self._break_even()

    def _pnl(self) -> np.ndarray:
        """Compute the total strategy PnL across the underlying prices.

        Returns:
            np.ndarray: Array of strategy PnL values.
        """

        strategy_pnl_values = np.zeros_like(self.underlying_prices)
        for option in self.options:
            strategy_pnl_values += option.pnl(self.underlying_prices)
        return strategy_pnl_values

    def _break_even(self) -> np.ndarray:
        """Calculate break-even points for the strategy.

        Returns:
            np.ndarray: Array of break-even points.
        """

        crossing_zero_indices = np.where(np.diff(np.sign(self.strategy_pnl_values)))[0]
        return self.underlying_prices[crossing_zero_indices]

    def plot(self, title: str = "Strategy PnL vs Underlying Price") -> None:
        """Plot the PnL of a strategy.

        Args:
            title (str): Plot title, default is "Strategy PnL vs Underlying Price".

        Returns:
            None
        """

        min_pnl = np.min(self.strategy_pnl_values)

        plt.figure(figsize=(10, 6))
        plt.plot(self.underlying_prices, self.strategy_pnl_values, label='Strategy PnL', color='blue')
        plt.axhline(y=0, color='gray', linestyle='--', label='Breakeven')

        # Plot break-even points
        plt.plot(self.break_even_underlying, np.zeros_like(self.break_even_underlying), 'ro', label='Breakeven Price')
        for be in self.break_even_underlying:
            plt.vlines(be, 0, min_pnl, color='red', linestyle='--')
            plt.text(be, min_pnl - 0.5, f'{be:.2f}', color='red', ha='center', va='top')

        plt.title(title)
        plt.xlabel('Underlying Price')
        plt.ylabel('PnL')
        plt.legend()
        plt.show()