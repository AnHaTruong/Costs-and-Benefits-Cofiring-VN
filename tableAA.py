# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
# Using the serialized ans object-oriented new code
#
""" Print table for the net present value calculation in  npv.py
"""

from units import time_horizon
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import discount_rate, depreciation_period, tax_rate

print('')

print('Time Horizon', time_horizon, 'years')
print('Discount Rate', discount_rate)
print('Depreciation', depreciation_period, 'years')


def printPlant(plant):
    print('')
    print(plant.name)
    print("NPV  =", plant.net_present_value(discount_rate, tax_rate, depreciation_period))
    plant.pretty_table(tax_rate, depreciation_period)
#    print("LCOE =", plant.lcoe(discount_rate, tax_rate, depreciation_period))

# printPlant(MongDuong1)
printPlant(MongDuong1Cofire)
# printPlant(NinhBinh)
printPlant(NinhBinhCofire)
