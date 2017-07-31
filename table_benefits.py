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

from init import TIMEHORIZON
from parameters import discount_rate, external_cost
from parameters import MongDuong1System, NinhBinhSystem


def benefits(system):
    """Tabulate the present value of various benefits from co-firing."""
    table = ['']
    table.append(system.cofiring_plant.name)
    table.append('-------------------')
    row2 = '{:30}' + '{:20.0f}'
    table.append(row2.format('Health', system.health_npv(discount_rate, external_cost)))
    table.append(row2.format('Emission reduction',
                             system.mitigation_npv(discount_rate, external_cost)))
    table.append(row2.format('Wages', system.wages_npv(discount_rate)))
    table.append(row2.format('Farmer earnings before tax',
                             system.farmer.net_present_value(discount_rate)))
    table.append(row2.format('Trader earnings before tax',
                             system.transporter.net_present_value(discount_rate)))
    return '\n'.join(table)


print("Total benefit over", TIMEHORIZON, "years")
print("Discounted at", discount_rate)
print("")
print(benefits(MongDuong1System))
print(benefits(NinhBinhSystem))
