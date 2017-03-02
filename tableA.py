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

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import discount_rate, depreciation_period, tax_rate
from units import time_horizon

print('')

print('Time Horizon', time_horizon, 'years')
print('Discount Rate', discount_rate)
print('Depreciation', depreciation_period, 'years')

print('')

MongDuong1.pretty_table(discount_rate, tax_rate, depreciation_period)

MongDuong1Cofire.pretty_table(discount_rate, tax_rate, depreciation_period)

print('')

NinhBinh.pretty_table(discount_rate, tax_rate, depreciation_period)

NinhBinhCofire.pretty_table(discount_rate, tax_rate, depreciation_period)
