# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Draw a figure showing the cumulative costs/benefits for different groups."""
import matplotlib.pyplot as plt

import numpy as np

from model.utils import MUSD, USD, t, display_as
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period, external_cost
from manuscript1.parameters import NinhBinhSystem, price_NB


def benefit_array(system):
    """Return the data to be plot."""
    job_benefit = system.wages_npv(discount_rate) / MUSD
    plant_benefit = (
        system.cofiring_plant.net_present_value(discount_rate, tax_rate, depreciation_period) -
        system.plant.net_present_value(discount_rate, tax_rate, depreciation_period)) / MUSD
    transporter_benefit = system.transporter.net_present_value(discount_rate) / MUSD
    farmer_benefit = system.farmer.net_present_value(discount_rate) / MUSD
    health_benefit = system.health_npv(discount_rate, external_cost) / MUSD
    climate_benefit = system.mitigation_npv(discount_rate, external_cost) / MUSD
    return np.array([transporter_benefit, plant_benefit, farmer_benefit,
                     job_benefit, climate_benefit, health_benefit])


def case(system, price_ref, price_fieldside, price_plantgate):
    """Return a system for a given pair of straw prices, along with a formatted legend."""
    price = price_ref._replace(biomass_plantgate=price_plantgate,
                               biomass_fieldside=price_fieldside)
    display_as(price.biomass_plantgate, 'USD/t')
    display_as(price.biomass_fieldside, 'USD/t')
    label = f'Straw {price.biomass_fieldside} field side, {price.biomass_plantgate} plant gate'
    system.clear_market(price)
    return benefit_array(system), label


dataA, labelA = case(NinhBinhSystem, price_NB, 30 * USD / t, 37.3 * USD / t)
dataB, labelB = case(NinhBinhSystem, price_NB, 10 * USD / t, 12 * USD / t)
dataC, labelC = case(NinhBinhSystem, price_NB, 10 * USD / t, 36 * USD / t)
title = f'Cofiring 5% straw in {NinhBinhSystem.plant.name} power plant'
NinhBinhSystem.clear_market(price_NB)   # Reset to default configuration for further uses

index = np.arange(6)
width = 0.3
plt.figure(figsize=(10, 5))
plt.barh(index + 2 * width, dataA, width, edgecolor='none', label=labelA, color='#ff4500')
plt.barh(index + 1 * width, dataB, width, edgecolor='none', label=labelB, color='navy')
plt.barh(index + 0 * width, dataC, width, edgecolor='none', label=labelC, color='green')
plt.title(title)
plt.xlabel('Cumulative benefit over 20 years (M$)')
plt.yticks(index + 0.2, ('Trader profit',
                         'Plant profit',
                         'Farmer profit',
                         'Workers wages\n(harvest, transport, O&M)',
                         'CO2 emission reduction\nvalued at 1$/tCO2',
                         'Local air quality\nmostly dust reduction'))
plt.legend(bbox_to_anchor=(0.98, 0.4), prop={'size': 12}, frameon=False)
plt.tight_layout()

plt.savefig("figure3.png")
