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

from model.utils import MUSD, USD, t
from model.system import System, label
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period, external_cost
from manuscript1.parameters import plant_parameter_NB, cofire_NB, supply_chain_NB, price_NB
from manuscript1.parameters import farm_parameter, transport_parameter


def benefit_array(system):
    """Return the data to be plot."""
    job_benefit = system.wages_npv(discount_rate) / MUSD
    plant_benefit = (system.cofiring_plant.net_present_value(discount_rate,
                                                             tax_rate,
                                                             depreciation_period)
                     - system.plant.net_present_value(discount_rate,
                                                      tax_rate,
                                                      depreciation_period)
                     ) / MUSD
    transporter_benefit = system.transporter.net_present_value(discount_rate) / MUSD
    farmer_benefit = system.farmer.net_present_value(discount_rate) / MUSD
    health_benefit = system.health_npv(discount_rate, external_cost) / MUSD
    climate_benefit = system.mitigation_npv(discount_rate, external_cost) / MUSD
    return np.array([transporter_benefit, plant_benefit, farmer_benefit,
                     job_benefit, climate_benefit, health_benefit])


def case(price_fieldside, price_plantgate):
    """Return a system for a given pair of straw prices, along with a formatted legend."""
    price = price_NB._replace(biomass_plantgate=price_plantgate,
                              biomass_fieldside=price_fieldside)
    system = System(plant_parameter_NB, cofire_NB, supply_chain_NB, price, farm_parameter,
                    transport_parameter)
    return system, label(price)


systemA, labelA = case(30 * USD / t, 37.26 * USD / t)
systemB, labelB = case(10 * USD / t, 12 * USD / t)
systemC, labelC = case(10 * USD / t, 36 * USD / t)

index = np.arange(6)
width = 0.3
plt.figure(figsize=(10, 5))
NB = plt.barh(index + 2 * width, benefit_array(systemA), width,
              color='#ff4500', edgecolor='none', label=labelA)
NB2 = plt.barh(index + width, benefit_array(systemB), width,
               color='navy', edgecolor='none', label=labelB)
NB3 = plt.barh(index, benefit_array(systemC), width,
               color='green', edgecolor='none', label=labelC)
plt.title('Cofiring 5% straw in Ninh Binh power plant')
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
