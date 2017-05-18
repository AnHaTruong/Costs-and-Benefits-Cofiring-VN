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
from parameters import discount_rate, tax_rate, depreciation_period, feedin_tarif
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import winder_rental_cost, straw, specific_cost

from parameters import winder_haul, truck_velocity, work_hour_day, truck_loading_time
from parameters import truck_load, OM_hour_MWh, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance, wage_bm_loading


def benefit_array(plant, cofiringplant, income_parameter):
    job_benefit = cofiringplant.wages_npv(discount_rate,
                                          work_hour_day,
                                          winder_haul,
                                          wage_bm_collect,
                                          truck_load,
                                          truck_velocity,
                                          wage_bm_transport,
                                          truck_loading_time,
                                          wage_bm_loading,
                                          OM_hour_MWh,
                                          wage_operation_maintenance)/USD/1000000
    plant_benefit = (cofiringplant.net_present_value(income_parameter,
                                                     discount_rate,
                                                     tax_rate,
                                                     depreciation_period)
                     - plant.net_present_value(income_parameter,
                                              discount_rate,
                                              tax_rate,
                                              depreciation_period)
                     )/USD/1000000
    farmer_benefit = cofiringplant.straw_supply.farm_npv(discount_rate,
                                                         winder_rental_cost,
                                                         straw.price)/USD/1000000
    health_benefit = cofiringplant.health_npv(discount_rate, specific_cost)/USD/1000000
    climate_benefit = cofiringplant.CO2_npv(discount_rate, specific_cost)/USD/1000000
    return np.array([plant_benefit, farmer_benefit, job_benefit, health_benefit, climate_benefit])

index = np.arange(5)
width = 0.4
plt.figure(figsize=(10,5))
MD = plt.barh(index, benefit_array(MongDuong1, MongDuong1Cofire, feedin_tarif['MD']), width,
              color='navy', edgecolor='none', label='Monng Duong 1')
NB = plt.barh(index + width, benefit_array(NinhBinh, NinhBinhCofire, feedin_tarif['NB']), width,
              color='#ff4500', edgecolor='none', label='Ninh Binh')
plt.xlabel('Cumulative benefit over 20 years (M$)')
plt.yticks(index+0.5, ('Plant onwer (net profit)',
                       'Farmer\n(sell straw)',
                       'Workers\n(harvest, transport, O&M)',
                       'Local society\n(Air quality)',
                       'Global society\n(GHG mitigation)'))
plt.legend(bbox_to_anchor=(0.98, 1.0), prop={'size': 10})
plt.tight_layout()

plt.savefig("Figure3.png")
