# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print table for the present value of benefit from co-firing added up
    in benefitaddup.py
"""
from init import time_horizon
from parameters import discount_rate
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import winder_rental_cost, straw, specific_cost

from parameters import winder_haul, truck_velocity, work_hour_day, truck_loading_time
from parameters import truck_load, OM_hour_MWh, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance, wage_bm_loading

from benefitaddup import benefit_add_up, total_benefit_addup
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit, total_health_benefit

from job import total_job_benefit

print("Total benefit over", time_horizon, "years")
print("Discounted at", discount_rate)
print("")


def print_benefit_add_up(plant, cofiringplant):
    print('')
    print(cofiringplant.name)
    print('-------------------')
    row2 = '{:30}' + '{:20.0f}' + '{:20.0f}'
    print(row2.format('Health',
                      benefit_add_up(total_health_benefit, plant, cofiringplant),
                      cofiringplant.health_npv(discount_rate, specific_cost)
                      )
          )
    print(row2.format('Emission reduction',
                      benefit_add_up(emission_reduction_benefit, plant, cofiringplant),
                      cofiringplant.CO2_npv(discount_rate, specific_cost)
                      )
          )

    print(row2.format('Jobs',
                      benefit_add_up(total_job_benefit, plant, cofiringplant),
                      cofiringplant.wages_npv(discount_rate,
                                              work_hour_day,
                                              winder_haul,
                                              wage_bm_collect,
                                              truck_load,
                                              truck_velocity,
                                              wage_bm_transport,
                                              truck_loading_time,
                                              wage_bm_loading,
                                              OM_hour_MWh,
                                              wage_operation_maintenance)
                      )
          )
    print(row2.format('Farmer income',
                      benefit_add_up(total_income_benefit, plant, cofiringplant),
                      cofiringplant.straw_supply.farm_npv(discount_rate,
                                                          winder_rental_cost,
                                                          straw.price)
                      )
          )
    print(row2.format('Total',
                      total_benefit_addup(plant, cofiringplant),
                      float('NaN')
                      )
          )

print_benefit_add_up(MongDuong1, MongDuong1Cofire)

print_benefit_add_up(NinhBinh, NinhBinhCofire)
