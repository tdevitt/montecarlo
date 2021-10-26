import matplotlib.pyplot as plt
import numpy as np
import math

from numpy.lib.stride_tricks import sliding_window_view

def EuropeanCallPayoff(underlying_price, strike_price):
    if underlying_price > strike_price:
        return underlying_price - strike_price
    else:
        return 0

def GeometricBrownianMotion_WithBarrier(initial_price, drift, volatility, timestep, total_time, barrier):
    prices = []
    barrier_checks = []
    current_price = initial_price

    while(total_time - timestep > 0):
        Z = np.random.normal(0,1)

        dSt = current_price * (drift*timestep + volatility*np.sqrt(timestep)*Z)
        current_price = current_price + dSt

        prices.append(current_price)
        if current_price >= barrier:
            barrier_checks.append(int(1))
        else:
            barrier_checks.append(int(0))
        
        total_time = total_time - timestep

    return prices, barrier_checks

risk_free_rate = .0115 #annualized rate corresponding to yield curve that matches tenor of the option
price = 10.0 #current price of underlying
annual_vol = 0.40 #estimate of forward looking annualized volatility
timestep_in_years = 1 / 252 #estimated trading days in calendar year is 252 (ex: 1/252 for daily timestep or 5/252 for weekly timestep)
timeframe_in_years = 5
annual_drift = 0.10 #expected annual return (or alternatively the asset specific discount rate); for option pricing this should equal the risk free rate (risk neutral model)

simulated_paths = []
final_underlying_prices = []

call_option_prices = []
strike = 11.5
redemption_barrier = 18.00 #price at which options can be called or redeemed
barrier_obs_window = 30
barrier_threshold = 20

risk_neutral_model = True

if risk_neutral_model == True:
    annual_drift = risk_free_rate

simulations = 1000
#generate list of underlying price paths and barrier crosses
for i in range(0, simulations):
    price_path, barrier_path = GeometricBrownianMotion_WithBarrier(price, annual_drift, annual_vol, timestep_in_years, timeframe_in_years, redemption_barrier)
    simulated_paths.append(price_path)
    
    window_sums = np.sum(sliding_window_view(barrier_path, window_shape=barrier_obs_window), axis=1) #use numpy function to do sum of barrier booleans in each barrier window
    idx_barrier_break = np.argmax(window_sums >= barrier_threshold) #use argmax function to get array location of first day in first barrier window where price is above redemption trigger
    
    if idx_barrier_break > 0:
        final_underlying_prices.append(price_path[idx_barrier_break+barrier_obs_window-1])
    else:
        final_underlying_prices.append(price_path[-1])

for px in final_underlying_prices:
    call_option_prices.append(EuropeanCallPayoff(px, strike) / pow(1 + risk_free_rate, timeframe_in_years)) #call prices discounted to present by risk free rate

avg_call_price = np.average(call_option_prices)
print("Average Call Price:", avg_call_price)

ticks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
plt.hist(call_option_prices, bins=ticks)
plt.xticks(ticks)
plt.show()