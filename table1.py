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

print('''
Table 1. Technical parameters
''')

row = '{:24}'+' {:>20}'*2

col1 = MongDuong1.coal_consumption
col2 = NinhBinh.coal_consumption
col1.display_unit = 't/y'
col2.display_unit = 't/y'


print('{:24}{:>20}{:>20}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))

print('{:24}{:>20}{:>20}'.format('Comissioning year', MongDuong1.commissioning, NinhBinh.commissioning))
print('{:24}{:>20}{:>20}'.format('Boiler technology', MongDuong1.boiler_technology, NinhBinh.boiler_technology))
print('{:24}{:>20.0f}{:>17.0f}'.format('Installed capacity', MongDuong1.capacity, NinhBinh.capacity))
print('{:24}{:>20.2f}{:>20.2f}'.format('Capacity factor', MongDuong1.capacity_factor, NinhBinh.capacity_factor))
print('{:24}{:>20.0f}{:>16.0f}'.format('Coal consumption',  col1, col2))
print('{:24}{:>20.0f}{:>14.0f}'.format('Heat value of coal', MongDuong1.coal.heat_value, NinhBinh.coal.heat_value))
print('{:24}{:>20.4f}{:>20.4f}'.format('Plant efficiency', MongDuong1.plant_efficiency[0], NinhBinh.plant_efficiency[0]))
print('{:24}{:>20.4f}{:>20.4f}'.format('Boiler efficiency', MongDuong1.boiler_efficiency[0], NinhBinh.boiler_efficiency[0]))
