from quant import *
from plot import *

TRADING_DAYS = 252

sigma = 0.89

underlying_price = 141.98
strike_price = 141
risk_free_rate = 0.045
days_to_expiration = 7
expiry = days_to_expiration / TRADING_DAYS
option_type = 'put' # call or put

# ('option_type', strike_price, premium_paid/received, time_to_expiry, contract_fee).
strategy = [
    ('put', 141, 6.50, expiry, 0.75),
    ('call', 142, 7.10, expiry, 0.75),
    ('call', 142, 11, expiry, 0.75),
]

option_price = binomial_model(underlying_price, strike_price, risk_free_rate, expiry, sigma, 1000, option_type)
print(f"The price of the option is: {option_price:.2f}")

plot_greeks_vs_underlying(underlying_price, strike_price, risk_free_rate, expiry, sigma, 1000, option_type)
plot_pnL(strategy, underlying_price, price_range=None)

plt.show()
