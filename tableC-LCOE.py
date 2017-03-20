# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity (LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Compares the LCOE with and without cofiring"""

from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import discount_rate, tax_rate, depreciation_period, feedin_tarif

MongDuong1.table_LCOE(feedin_tarif['MD'], discount_rate, tax_rate, depreciation_period)

MongDuong1Cofire.tableC(feedin_tarif['MD'], discount_rate, tax_rate, depreciation_period)

print('')

NinhBinh.table_LCOE(feedin_tarif['NB'], discount_rate, tax_rate, depreciation_period)

NinhBinhCofire.tableC(feedin_tarif['NB'], discount_rate, tax_rate, depreciation_period)
