import matplotlib.pyplot as plt
import numpy as np
import math

def GeometricBrownianMotion(initial_price, drift, volatility, timestep, total_time):
    prices = []
    current_price = initial_price

    while(total_time - timestep > 0):
        Z = np.random.normal(0,1)

        dSt = current_price * (drift*timestep + volatility*np.sqrt(timestep)*Z)
        current_price = current_price + dSt

        prices.append(current_price)
        total_time = total_time - timestep

    return prices

price = 10.0 #current price of underlying
annual_vol = 0.40 #estimate of forward looking annualized volatility
timestep_in_years = 1 / 252 #estimated trading days in calendar year is 252 
timeframe_in_years = 5
annual_drift = 0.10 #expected annual return (or alternatively the asset specific discount rate)

simulations = 100
simulated_paths = []
final_prices = []

for i in range(0, simulations):
    price_path = GeometricBrownianMotion(price, annual_drift, annual_vol, timestep_in_years, timeframe_in_years)
    simulated_paths.append(price_path)
    final_prices.append(price_path[-1])

avg_final_price = np.average(final_prices)
discounted_avg_final_price = avg_final_price / pow(1+annual_drift, timeframe_in_years)

print(avg_final_price)
print(np.median(final_prices))

for sim in simulated_paths:
    plt.plot(np.arange(0, len(sim)), sim)

plt.show()