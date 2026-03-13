# Morocco Power Market Simulation

## Overview
This project aims to simulate the impact of a hypothetical wind farm and industrial battery on the energy consumption of Tetouan city in Morocco. Key components involve simulating the workings of a wind farm and the operational behaviour of an industrial battery. This simulation is then run across the January and July months, and comparisons are made regarding shortfall impacts.

## Dataset
The dataset used contains a year of data from 2017, from 2017.01.01 00:00:00 - 2017.12.30 23:50:00, in 10 minute intervals. The variables included are Datetime, temperature, humidity, wind speed, general diffuse flows, diffuse flows, Zone 1 Power Consumption, Zone 2 Power Consumption and Zone 3 Power Consumption. This project focussed on using only Datetime, wind speed, and the sum of the zonal power consumption. 

The citation for this dataset is:

Salam, A., & El Hibaoui, A. (2018, December). Comparison of Machine Learning Algorithms for the Power Consumption Prediction:-Case Study of Tetouan city“. In 2018 6th International Renewable and Sustainable Energy Conference (IRSEC) (pp. 1-5). IEEE.

## Methodology
The key methods used are a wind farm model and a battery model. The wind farm model utilises key working components, such as wind power (wind speed ** 3), cut-in, rated speed and max capacity, to simulate the impact of varying wind speeds originating from the dataset. The battery model follows on from this, aiming to store any excess wind farm output not required for immediate consumption. 

The battery model uses discharge, rate limit, efficiency and capacity to simulate a realistic industrial battery. The mechanism behind whether to charge or discharge is also dependent on the net consumption (wind power minus total consumption). Using this information, shortfall and annual demand of wind energy and battery discharge as a percentage of total consumption is calculated.

## Key Findings

![Simulation Results]("C:\Users\ieddy\Downloads\Finalised Morocco Study Graph.png")

The main key finding from this project is the significant difference between January and July model outputs. January showed limited wind power output, apart from a ramp up towards the end of the month. This meant that total consumption was widely equal to total shortfall across the majority of January, with the pattern towards month-end showing shortfall being pushed lower than consumption. The battery was also not charged throughout the month due to this, largely running on 0% capacity.

On the other hand, July showed significant wind power output throughout the month, with a distinct pattern showing wind power making up a portion of total consumption, though shortfall being overall significant. While wind power was significantly more during this month, it was still not enough to enable battery charging.

Another key finding was the overall wind power and battery contribution to total consumption across the year was averaged at 11.6%. This shows that, while the use of wind farms and batteries have been found to contribute to overall total consumption, it is not at a level which can be dependent on by the city of Tetouan.

## Assumptions
Wind farm parameters: 30,000 kW capacity, cut-in 0.078 m/s, rated speed 5.5 m/s

Battery parameters: 30,000 kW capacity, 900 kW rate limit, 80% efficiency, 50% starting charge

## Requirements
Python 3.x, Pandas, matplotlib
