import numpy as np
import OptionQuant as oq

def example():
    """
    This function demonstrates how to use the OptionQuant library to:
    - Define options with specific parameters.
    - Create an option strategy with multiple options.
    - Price the options using the Binomial model.
    - Plot the strategy PnL.
    """

    # -------------------------- Step 1: Define Options --------------------------
    # Create a put option (option1) and a call option (option2)
    # The parameters are: <option_type>, <strike>, <underlying_price>, <premium>, <time_to_expiry>, <sigma>, <contract_fee>, <is_american>
    
    option1 = oq.Option(option_type='put', strike=140, underlying_price=141, premium=8.15, 
                        time_to_expiry=2, sigma=1.07, contract_fee=0.75, is_american=True)
    
    option2 = oq.Option(option_type='call', strike=140, underlying_price=142, premium=5.80, 
                        time_to_expiry=2, sigma=1.07, contract_fee=0.75, is_american=False)

    # Print out the option details (for user reference)
    print(f"Option1 (Put) details: {option1}")
    print(f"Option2 (Call) details: {option2}")

    # ---------------------- Step 2: Create Option Strategy ----------------------
    # Define the strategy by including both options and providing a range of underlying prices.
    # The strategy will evaluate its PnL at these prices (from 130 to 150).

    underlying_prices = np.linspace(130, 150, 1000)  # 1000 points between 130 and 150 for simulation
    strategy = oq.OptionStrategy(options=[option1, option2], underlying_prices=underlying_prices)

    # Print strategy details (for user reference)
    print(f"Strategy details: {strategy}")

    # ------------------ Step 3: Price Options using the Binomial Model ------------
    # Calculate the theoretical price of option1 (Put) and option2 (Call) using the Binomial model.
    # This uses the OptionPricer class to apply the binomial model pricing technique.
    
    price_option1_binomial = oq.OptionPricer.binomial_model(option1, N=1000)  # N=1000 for the number of time steps
    price_option2_binomial = oq.OptionPricer.binomial_model(option2, N=1000)

    # Print the calculated Binomial model prices for both options
    print(f"Price of Option1 (Put) using Binomial Model: {price_option1_binomial:.2f}")
    print(f"Price of Option2 (Call) using Binomial Model: {price_option2_binomial:.2f}")

    # ---------------- Step 4: (Optional) Price Options using Black-Scholes-Merton Model
    
    price_option1_bsm = oq.OptionPricer.black_scholes_merton(option1, risk_free_rate=0.04)
    price_option2_bsm = oq.OptionPricer.black_scholes_merton(option2, risk_free_rate=0.04)

    # Print the calculated Black-Scholes-Merton model prices (if using)
    print(f"Price of Option1 (Put) using Black-Scholes-Merton: {price_option1_bsm:.2f}")
    print(f"Price of Option2 (Call) using Black-Scholes-Merton: {price_option2_bsm:.2f}")

    # ----------------- Step 5: Plot Strategy PnL ------------------------------
    # Once we have priced the options, we plot the strategy's PnL against the range of underlying prices.
    # This visualizes how the strategy behaves at different price points for the underlying asset.

    strategy.plot()

if __name__ == "__main__":
    # Run the example function if this script is executed directly
    example()