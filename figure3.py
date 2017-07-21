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
""" Draw Figure 3 to visualize table 12 added up benefits for different group
"""

import matplotlib.pyplot as plt
import numpy as np
from init import USD
from parameters import discount_rate, tax_rate, depreciation_period, feedin_tariff
from parameters import MongDuong1System, NinhBinhSystem
from parameters import specific_cost


def benefit_array(system, income_parameter):
    MUSD = 10**6 * USD
    job_benefit = system.wages_npv(discount_rate) / MUSD
    plant_benefit = (system.cofiring_plant.net_present_value(income_parameter,
                                                             discount_rate,
                                                             tax_rate,
                                                             depreciation_period)
                     - system.plant.net_present_value(income_parameter,
                                                      discount_rate,
                                                      tax_rate,
                                                      depreciation_period)
                     ) / MUSD
    farmer_benefit = system.farmer.npv(discount_rate) / MUSD
    health_benefit = system.health_npv(discount_rate, specific_cost) / MUSD
    climate_benefit = system.CO2_npv(discount_rate, specific_cost) / MUSD
    return np.array([plant_benefit, farmer_benefit, job_benefit, health_benefit, climate_benefit])


index = np.arange(5)
width = 0.4
plt.figure(figsize=(10, 5))
NB = plt.barh(index + width, benefit_array(NinhBinhSystem, feedin_tariff['NB']), width,
              color='#ff4500', edgecolor='none', label='Ninh Binh')
MD = plt.barh(index, benefit_array(MongDuong1System, feedin_tariff['MD']), width,
              color='navy', edgecolor='none', label='Mong Duong 1')
plt.xlabel('Cumulative benefit over 20 years (M$)')
plt.yticks(index + 0.5, ('Plant owner\n(net profit)',
                         'Farmer\n(sell straw)',
                         'Workers\n(harvest, transport, O&M)',
                         'Local society\n(air quality)',
                         'Global society\n(GHG mitigation)'))
plt.legend(bbox_to_anchor=(0.98, 0.4), prop={'size': 12}, frameon=False)
plt.tight_layout()

plt.savefig("figure3.png")
