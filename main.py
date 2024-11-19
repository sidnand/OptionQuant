import numpy as np

import OptionQuant as oq

# Define options (<option_type>, <strike>, <underlying_price>, <sigma>, <time_to_expiry>, <dividend_yield>, <risk_free_rate>, <is_american>)
option1 = oq.Option('put', 140, 141, 8.15, 2, 1.07, 0.75, True)
option2 = oq.Option('call', 140, 142, 5.80, 2, 1.07, 0.75)

# Strategy
strategy = oq.OptionStrategy([option1, option2],
                             np.linspace(130, 150, 1000))

# get binomial model price
price_option1 = oq.OptionPricer.binomial_model(option1, 0.04)
price_option2 = oq.OptionPricer.binomial_model(option2, 0.04)

# price_option1_black_scholes = oq.OptionPricer.black_scholes_merton(option1, 0.04)
# price_option2_black_scholes = oq.OptionPricer.black_scholes_merton(option2, 0.04)

# Plot
strategy.plot()
