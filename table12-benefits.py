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
""" Print table for the present value of benefit from co-firing added up"""

from init import time_horizon
from parameters import discount_rate
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import straw, specific_cost
from parameters import collect_economics, truck_economics, OM_economics

print("Total benefit over", time_horizon, "years")
print("Discounted at", discount_rate)
print("")


def print_benefit_add_up(plant, cofiringplant):
    print('')
    print(cofiringplant.name)
    print('-------------------')
    row2 = '{:30}' + '{:20.0f}'
    print(row2.format('Health',
                      cofiringplant.health_npv(discount_rate, specific_cost)
                      )
          )
    print(row2.format('Emission reduction',
                      cofiringplant.CO2_npv(discount_rate, specific_cost)
                      )
          )

    print(row2.format('Jobs',
                      cofiringplant.wages_npv(discount_rate, collect_economics, truck_economics,
                                              OM_economics)
                      )
          )
    print(row2.format('Farmer income',
                      cofiringplant.straw_supply.farm_npv(discount_rate,
                                                          straw.price,
                                                          collect_economics,
                                                          truck_economics)
                      )
          )


print_benefit_add_up(MongDuong1, MongDuong1Cofire)

print_benefit_add_up(NinhBinh, NinhBinhCofire)
