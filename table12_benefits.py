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
"""Print table for the present value of benefit from co-firing added up."""

from init import time_horizon
from parameters import discount_rate, external_cost
from parameters import MongDuong1System, NinhBinhSystem


print("Total benefit over", time_horizon, "years")
print("Discounted at", discount_rate)
print("")


def print_benefit_add_up(system):
    """Print table for the present value of benefit from co-firing added up."""
    print('')
    print(system.cofiring_plant.name)
    print('-------------------')
    row2 = '{:30}' + '{:20.0f}'
    print(row2.format('Health', system.health_npv(discount_rate, external_cost)))
    print(row2.format('Emission reduction', system.CO2_npv(discount_rate, external_cost)))
    print(row2.format('Wages', system.wages_npv(discount_rate)))
    print(row2.format('Farmer earnings before tax',
                      system.farmer.net_present_value(discount_rate)))
    print(row2.format('Trader earnings before tax',
                      system.transporter.net_present_value(discount_rate)))


print_benefit_add_up(MongDuong1System)

print_benefit_add_up(NinhBinhSystem)
