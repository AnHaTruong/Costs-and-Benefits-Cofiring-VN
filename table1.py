# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print table 1 for Technical parameters of the plants"""

from parameters import MongDuong1, NinhBinh

print('')
print('Table 1. Technical parameters')

head = '{:24}'+' {:>20}'*2
row = '{:24}'+' {:>20}'*2

col1 = MongDuong1.coal_consumption
col2 = NinhBinh.coal_consumption
col1.display_unit = 't/y'
col2.display_unit = 't/y'


print(head.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))

print(row.format('Comissioning year', MongDuong1.commissioning, NinhBinh.commissioning))
print(row.format('Boiler technology', MongDuong1.boiler_technology, NinhBinh.boiler_technology))
print(row.format('Installed capacity', MongDuong1.capacity, NinhBinh.capacity))
print(row.format('Capacity factor', MongDuong1.capacity_factor, NinhBinh.capacity_factor))
print(row.format('Coal consumption',  col1, col2))
print(row.format('Heat value of coal', MongDuong1.coal_supply.heat_value, NinhBinh.coal_supply.heat_value))
print(row.format('Plant efficiency', MongDuong1.plant_efficiency, NinhBinh.plant_efficiency))
print(row.format('Boiler efficiency', MongDuong1.boiler_efficiency, NinhBinh.boiler_efficiency))
