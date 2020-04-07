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

from model.utils import MUSD, USD, t, display_as, array, arange
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period, external_cost
from manuscript1.parameters import NinhBinhSystem, price_NB


def benefit_array(system):
    """Return the data to be plot."""
    job_benefit = system.wages_npv(discount_rate) / MUSD
    plant_benefit = (
        system.cofiring_plant.net_present_value(discount_rate, tax_rate, depreciation_period) -
        system.plant.net_present_value(discount_rate, tax_rate, depreciation_period)) / MUSD
    reseller_benefit = system.reseller.net_present_value(discount_rate) / MUSD
    farmer_benefit = system.farmer.net_present_value(discount_rate) / MUSD
    health_benefit = system.health_npv(discount_rate, external_cost) / MUSD
    climate_benefit = system.mitigation_npv(discount_rate, external_cost) / MUSD
    return array([reseller_benefit, plant_benefit, farmer_benefit,
                  job_benefit, climate_benefit, health_benefit])


def case(system, price_ref, p_fieldside, p_plantgate):
    """Return a system for a given pair of straw prices, along with a formatted legend."""
    price = price_ref._replace(biomass_plantgate=p_plantgate,
                               biomass_fieldside=p_fieldside)
    display_as(price.biomass_plantgate, 'USD/t')
    display_as(price.biomass_fieldside, 'USD/t')
    label = ('Straw ' + str(price.biomass_fieldside) + ' field side, ' +
             str(price.biomass_plantgate) + ' plant gate')
    system.clear_market(price)
    data = benefit_array(system)
    system.clear_market(price_ref)
    return data, label


dataA, labelA = case(NinhBinhSystem, price_NB, 30 * USD / t, 37.3 * USD / t)
dataB, labelB = case(NinhBinhSystem, price_NB, 15 * USD / t, 17 * USD / t)
dataC, labelC = case(NinhBinhSystem, price_NB, 15 * USD / t, 36 * USD / t)
title = 'Cofiring 5% straw in ' + str(NinhBinhSystem.plant.name) + ' power plant'

index = arange(6)
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
plt.legend(bbox_to_anchor=(0.98, 0.4),
           prop={'size': 12},
           frameon=False)
plt.tight_layout()

plt.savefig("figure_benefits.svg")
