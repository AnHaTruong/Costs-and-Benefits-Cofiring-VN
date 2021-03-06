# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# table_uncertainty
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Print the table of parameters values used for the sensitivity analysis."""

from pandas import set_option
from sensitivity.uncertainty import uncertainty_MD1, uncertainty_NB

set_option("display.float_format", "{:9,.2f}".format)

print("Parameters values for the sensitivity analysis.")
print()
print("Mong Duong 1")
print(uncertainty_MD1)
print()
print("Ninh Binh")
print(uncertainty_NB)
