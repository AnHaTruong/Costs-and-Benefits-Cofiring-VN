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

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import feedin_tarif
from parameters import discount_rate, depreciation_period, tax_rate
from init import time_horizon

print('')

print('Time Horizon', time_horizon, 'years')
print('Discount Rate', discount_rate)
print('Depreciation', depreciation_period, 'years')

print('')
print('FIT', feedin_tarif['MD'])
MongDuong1.pretty_table(feedin_tarif['MD'], discount_rate, tax_rate, depreciation_period)

MongDuong1Cofire.pretty_table(feedin_tarif['MD'], discount_rate, tax_rate, depreciation_period)

print('')

print('FIT', feedin_tarif['NB'])
NinhBinh.pretty_table(feedin_tarif['NB'], discount_rate, tax_rate, depreciation_period)

NinhBinhCofire.pretty_table(feedin_tarif['NB'], discount_rate, tax_rate, depreciation_period)
