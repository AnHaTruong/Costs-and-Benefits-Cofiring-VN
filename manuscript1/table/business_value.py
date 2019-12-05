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
from pandas import concat

from manuscript1.parameters import MongDuong1System, NinhBinhSystem, discount_rate

from model.wtawtp import feasibility_direct

print('Business value of cofiring, from project NPVs.\n')
print(concat([
    MongDuong1System.table_business_value(discount_rate),
    NinhBinhSystem.table_business_value(discount_rate)],
    axis=1))

print("""

Business value of cofiring, from WTA, WTP and other per t values.
""")

print(concat([
    feasibility_direct(MongDuong1System, discount_rate),
    feasibility_direct(NinhBinhSystem, discount_rate)],
    axis=1))
