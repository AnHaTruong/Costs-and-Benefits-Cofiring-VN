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

print('')

print("Mong Duong 1 - no cofiring")
MongDuong1.pretty_table(tax_rate, depreciation_period)
print("NPV  =", MongDuong1.net_present_value(discount_rate, tax_rate, depreciation_period))
print("LCOE =", MongDuong1.lcoe(discount_rate, tax_rate, depreciation_period))

print("\nMong Duong 1 - cofiring")
MongDuong1Cofire.pretty_table(tax_rate, depreciation_period)
print("NPV  =", MongDuong1Cofire.net_present_value(discount_rate, tax_rate, depreciation_period))
print("LCOE =", MongDuong1Cofire.lcoe(discount_rate, tax_rate, depreciation_period))

print("\nNinh Binh - no cofiring")
NinhBinh.pretty_table(tax_rate, depreciation_period)
print("NPV  =", NinhBinh.net_present_value(discount_rate, tax_rate, depreciation_period))
print("LCOE =", NinhBinh.lcoe(discount_rate, tax_rate, depreciation_period))

print("\nNinh Binh - cofiring")
NinhBinhCofire.pretty_table(tax_rate, depreciation_period)
print("NPV  =", NinhBinhCofire.net_present_value(discount_rate, tax_rate, depreciation_period))
print("LCOE =", NinhBinhCofire.lcoe(discount_rate, tax_rate, depreciation_period))
