# Option Analysis Tool

1. Price an American option using the Binomial Tree Model.
2. Plot your option strategy and see ther PnL and break-even point.
3. Visualize the option greeks and see how they change with the underlying price.

## Usage

You can work directly from `main.py`

```python
TRADING_DAYS = 252

sigma = <implied volatility of the underlying>

underlying_price = <current price of the underlying>
strike_price = <strike price of the option>
risk_free_rate = <risk free rate, usually 3mo T-Bill>
days_to_expiration = <days to expiration>
expiry = days_to_expiration / TRADING_DAYS
option_type = <'call' or 'put'>

# ('option_type', strike_price, premium_paid/received, time_to_expiry, contract_fee)
strategy = [
    ('option_type', strike_price, premium_paid/received, time_to_expiry, contract_fee)
]

option_price = binomial_model(underlying_price, strike_price, risk_free_rate, expiry, sigma, 1000, option_type)
print(f"The price of the option is: {option_price:.2f}")

plot_greeks_vs_underlying(underlying_price, strike_price, risk_free_rate, expiry, sigma, 1000, option_type)
plot_pnL(strategy, underlying_price, price_range=None)

plt.show()
```
