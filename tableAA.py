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

from parameters import MongDuong1, NinhBinh, discount_rate, depreciation_period, tax_rate

print("Mong Duong 1 - no cofiring")
MongDuong1.pretty_table(tax_rate, depreciation_period)
print("NPV  =", MongDuong1.net_present_value(discount_rate, tax_rate, depreciation_period))
print("LCOE =", MongDuong1.lcoe(discount_rate, tax_rate, depreciation_period))

print("\nNinh Binh - no cofiring")
NinhBinh.pretty_table(tax_rate, depreciation_period)
print("NPV  =", NinhBinh.net_present_value(discount_rate, tax_rate, depreciation_period))
print("LCOE =", NinhBinh.lcoe(discount_rate, tax_rate, depreciation_period))
