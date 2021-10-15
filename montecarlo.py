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

price = 10.0
annual_vol = 0.35
timestep_in_years = 1 / 365
timeframe_in_years = 1
annual_drift = 0.10

price_path = GeometricBrownianMotion(price, annual_drift, annual_vol, timestep_in_years, timeframe_in_years)

print(price_path)