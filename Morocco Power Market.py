# -*- coding: utf-8 -*-
"""
Author: Isaac Eddy

Using following dataset: https://mavenanalytics.io/data-playground/morocco-electricity-consumption
2017.01.01 00:00:00 - 2017.12.30 23:50:00
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/ieddy/OneDrive/Documents/Python Scripts/powerconsumption.csv", parse_dates=["Datetime"])
df = df.sort_values("Datetime").reset_index(drop=True)

df["total_consumption"] = df["PowerConsumption_Zone1"] + df["PowerConsumption_Zone2"] + df["PowerConsumption_Zone3"]

print(df.isnull().sum()) # counts number of missing data per column

### Calculate wind power
# Wind farm parameters: 30,000 kW capacity, cut-in 0.078 m/s, rate speed 5.5 m/s
def calculate_wind_power(wind_speed):
    cut_in = 0.078
    rated_speed = 5.5
    max_capacity = 30000
    if wind_speed < cut_in:
        power = 0
    elif wind_speed >= rated_speed:
        power = max_capacity
    else:
        power = max_capacity * (wind_speed / rated_speed) ** 3
    return power

df["wind_power"] = df["WindSpeed"].apply(calculate_wind_power)

### Battery simulation
# Battery parameters: 30,000 kW capacity, 900 kW rate limit, 80% efficiency, 50% starting charge
def calculate_battery_charge(wind_power, total_consumption, capacity, rate_limit, efficiency, starting_charge):
    current_charge = starting_charge
    results = []
    discharge_results = []
    for i in range(len(df)):
        if current_charge == capacity and wind_power[i] > total_consumption[i]:
            discharge = 0
            current_charge = capacity
        elif wind_power[i] > total_consumption[i]:
            discharge = 0
            current_charge = min(current_charge + rate_limit * efficiency, capacity)
        elif wind_power[i] < total_consumption[i]:
            previous_charge = current_charge
            current_charge = max(current_charge - rate_limit * efficiency, 0)
            discharge = previous_charge - current_charge
        else:   
             current_charge = 0
             discharge = 0
        results.append(current_charge)
        discharge_results.append(discharge)
    return results, discharge_results
    
df["current_charge"], df["discharge"] = calculate_battery_charge(df["wind_power"], df["total_consumption"], 30000, 900, 0.8, 15000)
df["shortfall"] = df["total_consumption"] - df["wind_power"] - df["discharge"]
percentage_covered_annual_demand = ((df["wind_power"].sum() + df["discharge"].sum()) / df["total_consumption"].sum()) * 100

print(f"Annual demand covered by wind and battery: {percentage_covered_annual_demand:.1f}%")

### Data visualisation
df_january = df[df["Datetime"].dt.month == 1]
df_july = df[df["Datetime"].dt.month == 7]
    
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
ax1.plot(df_january["Datetime"], df_january["total_consumption"], label="Total Consumption")
ax1.plot(df_january["Datetime"], df_january["shortfall"], label="Shortfall")
ax1.legend()
ax1.set_title("Total Consumption and Shortfall of January 2017")
ax1.set_xlabel("Date")
ax1.tick_params(axis='x', rotation=45)
ax1.set_ylabel("Power (kW)")
ax3.plot(df_january["Datetime"], df_january["wind_power"], label="Wind Power")
ax3.plot(df_january["Datetime"], df_january["discharge"], label="Discharge")
ax3.legend()
ax3.set_title("Wind Power and Battery Discharge of January 2017")
ax3.set_xlabel("Date")
ax3.tick_params(axis='x', rotation=45)
ax3.set_ylabel("Power (kW)")

ax2.plot(df_july["Datetime"], df_july["total_consumption"], label="Total Consumption")
ax2.plot(df_july["Datetime"], df_july["shortfall"], label="Shortfall")
ax2.legend()
ax2.set_title("Total Consumption and Shortfall of July 2017")
ax2.set_xlabel("Date")
ax2.tick_params(axis='x', rotation=45)
ax2.set_ylabel("Power (kW)")
ax4.plot(df_july["Datetime"], df_july["wind_power"], label="Wind Power")
ax4.plot(df_july["Datetime"], df_july["discharge"], label="Discharge")
ax4.legend()
ax4.set_title("Wind Power and Battery Discharge of July 2017")
ax4.set_xlabel("Date")
ax4.tick_params(axis='x', rotation=45)
ax4.set_ylabel("Power (kW)")

plt.tight_layout()
plt.show()
    
    
    
    
