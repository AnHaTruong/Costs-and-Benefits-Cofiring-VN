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
""" Details the net present value calculations """

from init import time_horizon
from parameters import MongDuong1System, NinhBinhSystem
from parameters import price_MD, price_NB, discount_rate, depreciation_period, tax_rate

print('')

print('Time Horizon', time_horizon, 'years')
print('Discount Rate', discount_rate)
print('Depreciation', depreciation_period, 'years')

print('')
print('FIT', price_MD.electricity)
MongDuong1System.plant.pretty_table(discount_rate, tax_rate, depreciation_period)

MongDuong1System.cofiring_plant.pretty_table(discount_rate, tax_rate, depreciation_period)

print('')

print('FIT', price_NB.electricity)
NinhBinhSystem.plant.pretty_table(discount_rate, tax_rate, depreciation_period)

NinhBinhSystem.cofiring_plant.pretty_table(discount_rate, tax_rate, depreciation_period)
