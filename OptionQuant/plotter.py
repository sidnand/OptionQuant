import numpy as np
import matplotlib.pyplot as plt

class StrategyPlotter:
    @staticmethod
    def plot_strategy_pnl(strategy_pnl_values: np.ndarray,
                        break_even_underlying: np.ndarray,
                        title: str = "Strategy PnL vs Underlying Price") -> None:
        """Plot the PnL of a strategy.
        
        Args:
            strategy_pnl_values (np.ndarray): Array of strategy PnL values.
            break_even_underlying (np.ndarray): Array of break-even underlying prices.
            title (str): Plot title, default is "Strategy PnL vs Underlying Price".
            
        Returns:
            None
        """
        
        underlying_prices = np.linspace(0, len(strategy_pnl_values), len(strategy_pnl_values))
        min_pnl = np.min(strategy_pnl_values)


        plt.figure(figsize=(10, 6))
        plt.plot(underlying_prices, strategy_pnl_values, label='Strategy PnL', color='blue')
        plt.axhline(y=0, color='gray', linestyle='--', label='Breakeven')

        plt.plot(break_even_underlying, np.zeros_like(break_even_underlying), 'ro', label='Breakeven Price')
        for be in break_even_underlying:
            plt.vlines(be, 0, min_pnl, color='red', linestyle='--')
            plt.text(be, min_pnl - 0.5, f'{be:.2f}', color='red', ha='center', va='top')

        plt.title(title)
        plt.xlabel('Underlying Price')
        plt.ylabel('PnL')
        plt.legend()
        plt.show()