# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2019
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Draw a figure showing the cumulative costs/benefits for different groups."""

import matplotlib.pyplot as plt

import numpy as np

from init import MUSD
from parameters import discount_rate, tax_rate, depreciation_period, external_cost
from parameters import MongDuong1System, NinhBinhSystem


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
    return np.array([plant_benefit, transporter_benefit, farmer_benefit,
                     job_benefit, health_benefit, climate_benefit])


index = np.arange(6)
width = 0.4
plt.figure(figsize=(10, 5))
NB = plt.barh(index + width, benefit_array(NinhBinhSystem), width,
              color='#ff4500', edgecolor='none', label='Ninh Binh')
MD = plt.barh(index, benefit_array(MongDuong1System), width,
              color='navy', edgecolor='none', label='Mong Duong 1')
plt.xlabel('Cumulative benefit over 20 years (M$)')
plt.yticks(index + 0.5, ('Plant owner\n(net profit)',
                         'Trader\n(transport straw)',
                         'Farmer\n(sell straw)',
                         'Workers\n(harvest, transport, O&M)',
                         'Local society\n(air quality)',
                         'Global society\n(GHG mitigation)'))
plt.legend(bbox_to_anchor=(0.98, 0.4), prop={'size': 12}, frameon=False)
plt.tight_layout()

plt.savefig("figure3.png")
