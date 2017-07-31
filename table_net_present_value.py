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
"""Print details of the net present value calculations."""

from init import TIMEHORIZON
from parameters import MongDuong1System, NinhBinhSystem
from parameters import price_MD1, price_NB, discount_rate, depreciation_period, tax_rate

print('')

print('Time Horizon', TIMEHORIZON, 'years')
print('Discount Rate', discount_rate)
print('Depreciation', depreciation_period, 'years')

print('')
print('FIT', price_MD1.electricity)
print(MongDuong1System.plant.pretty_table(discount_rate, tax_rate, depreciation_period))
print(MongDuong1System.cofiring_plant.pretty_table(discount_rate, tax_rate, depreciation_period))

print('')

print('FIT', price_NB.electricity)
print(NinhBinhSystem.plant.pretty_table(discount_rate, tax_rate, depreciation_period))
print(NinhBinhSystem.cofiring_plant.pretty_table(discount_rate, tax_rate, depreciation_period))
