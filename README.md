# OptionQuant: A Python Package for Option Pricing and Strategy Analysis

OptionQuant is a Python package designed to assist in the pricing and analysis of financial options. It includes functionality for various option pricing models, including the Binomial and Black-Scholes-Merton models. Additionally, the package provides tools for defining option strategies and visualizing their profit and loss (PnL) across a range of underlying prices.

## Installation

To install `OptionQuant`, you can either clone this repository or install it directly from PyPI (if published):

```bash
git clone https://github.com/yourusername/OptionQuant.git
cd OptionQuant
python setup.py install
```

## Usage

### Option

The `Option` class allows you to define the properties of an individual option contract (either 'call' or 'put') and calculate its profit/loss (PnL) based on various underlying prices.

#### Example Usage

```python
import OptionQuant as oq

# Define an option: (option_type, strike, underlying_price, premium, time_to_expiry, sigma, contract_fee, is_american)
option1 = oq.Option('put', 140, 141, 8.15, 2, 1.07, 0.75, True)

# Get PnL for the option across a range of underlying prices
pnl_values = option1.pnl()

# Print the PnL
print(pnl_values)
```

### Option Strategy

The `OptionStrategy` class allows you to create strategies by combining multiple options. You can calculate and plot the strategy's total PnL across a range of underlying asset prices.

```python
import numpy as np
import OptionQuant as oq

# Define multiple options
option1 = oq.Option('put', 140, 141, 8.15, 2, 1.07, 0.75, True)
option2 = oq.Option('call', 140, 142, 5.80, 2, 1.07, 0.75)

# Define the strategy with a range of underlying prices
strategy = oq.OptionStrategy([option1, option2], np.linspace(130, 150, 1000))

# Plot the strategy's PnL
strategy.plot()
```

### Option Pricing

The `OptionPricer` class provides methods for pricing options using the Binomial and Black-Scholes-Merton models.

#### Example Usage (Binomial Model)

```python
import OptionQuant as oq

option1 = oq.Option('put', 140, 141, 8.15, 2, 1.07, 0.75, True)

# Price the option using the Binomial Model
binomial_price = oq.OptionPricer.binomial_model(option1, risk_free_rate=0.04)
print(f"Option Price (Binomial): {binomial_price}")
```

#### Example Usage (Black-Scholes-Merton Model)

```python
option1 = oq.Option('call', 140, 141, 5.80, 2, 1.07, 0.75)

# Price the option using the Black-Scholes-Merton Model
bs_price = oq.OptionPricer.black_scholes_merton(option1, risk_free_rate=0.04)
print(f"Option Price (Black-Scholes-Merton): {bs_price}")
```

### Strategy Plotter

The `StrategyPlotter` class provides a method to visualize the strategy's PnL across a range of underlying prices. This is useful to analyze potential outcomes and break-even points for a given strategy.

```python
import OptionQuant as oq

# Define your options and strategy as before
option1 = oq.Option('put', 140, 141, 8.15, 2, 1.07, 0.75, True)
option2 = oq.Option('call', 140, 142, 5.80, 2, 1.07, 0.75)
strategy = oq.OptionStrategy([option1, option2], np.linspace(130, 150, 1000))

# Use the StrategyPlotter to visualize the strategy's PnL
oq.StrategyPlotter.plot_strategy_pnl(strategy.strategy_pnl_values, strategy.break_even_underlying)
```

## Development

OptionQuant is using Python 3.13.0. After cloning the repo, setting up a virtual environment and installing the dependencies, read the Module section below to understand the structure of the package.

## Modules

### option.py

Defines the `Option` class, which represents an individual option contract. It provides functionality for calculating the profit and loss (PnL) based on underlying prices and option parameters.

Key Functions:

- `pnl`: Calculates the PnL for the option based on underlying prices.

### pricer.py

Defines the `OptionPricer` class, which includes methods to price options using the Binomial model and the Black-Scholes-Merton model.

Key Functions:

- `binomial_model`: Prices an option using the Binomial Option Pricing Model.
- `black_scholes_merton`: Prices an option using the Black-Scholes-Merton model.

### strategy.py

Defines the `OptionStrategy` class, which allows you to combine multiple options into a single strategy. It computes the total PnL of the strategy and identifies break-even points.

Key Functions:

- `_pnl`: Computes the total strategy PnL.
- `_break_even`: Identifies the break-even points of the strategy.
- `plot`: Plots the strategy’s PnL vs underlying price.

### plotter.py

Defines the `StrategyPlotter` class, which provides functionality to plot the strategy's PnL against underlying prices and mark the break-even points.

Key Functions:

- `plot_strategy_pnl`: Plots the strategy's PnL and break-even points.

## License

This package is licensed under the MIT License. See the LICENSE file for more details.
