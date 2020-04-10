# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Print the tables for manuscript 'Costs and benefits of co-firing'.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017-2019
"""

from manuscript1.parameters import (
    discount_rate,
    tax_rate,
    depreciation_period,
    coal_import_price,
)
from model.utils import display_as


print("Discount rate         ", discount_rate)
print("Tax rate              ", tax_rate)
print("Depreciation period   ", depreciation_period)
print("Coal import price     ", display_as(coal_import_price, "USD/t"))
