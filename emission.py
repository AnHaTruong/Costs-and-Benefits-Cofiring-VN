
# Economic of co-firing in two power plants in Vietnam
#
#  Greenhouse gas emissions reduction assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Greenhouse gas and pollutant emissions assessment of a co-firing project.
   Total emission include emission from fuel combustion, fuel transportation and open field burning
   Climate benefit and health benefit from GHG and air pollutant emission reduction
"""
import pandas as pd
from init import display_as
from parameters import specific_cost


def emission_reduction(plant, cofireplant):
    plant_ER = plant.stack.emissions()['Total'] - cofireplant.stack.emissions()['Total']
    transport_ER = (plant.coal_transporter().emissions()['Total'] -
                    cofireplant.coal_transporter().emissions()['Total'] -
                    cofireplant.straw_supply.transport_emissions()['Total']
                    )
    field_ER = (cofireplant.straw_supply.field_emission(cofireplant.biomass_used[0])['Total'] -
                cofireplant.straw_supply.field_emission(cofireplant.biomass_used)['Total']
                )
    total_ER = plant_ER + transport_ER + field_ER
    total_benefit = total_ER * specific_cost
    for pollutant in total_benefit:
        display_as(pollutant, 'kUSD')
    list_of_series = [plant_ER, transport_ER, field_ER, total_ER, total_benefit]
    row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
    ER_table = pd.DataFrame(list_of_series, index=row)
    return ER_table


def emission_reduction_benefit(plant, cofireplant):
    return emission_reduction(plant, cofireplant)['CO2']['Benefit']


def total_health_benefit(plant, cofireplant):
    return emission_reduction(plant, cofireplant).ix['Benefit'].drop('CO2').sum()
