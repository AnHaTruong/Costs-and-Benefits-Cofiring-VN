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
""" Print table 1 for Technical parameters of the plants"""

from init import isclose
from parameters import MongDuong1System, NinhBinhSystem

print("\nTable 5. Straw required and straw cost estimation\n")

col3 = MongDuong1System.biomass_used[1]
col4 = NinhBinhSystem.biomass_used[1]

col5 = MongDuong1System.sourcing_cost_per_t()[1]
col6 = NinhBinhSystem.sourcing_cost_per_t()[1]

col9 = MongDuong1System.transport_cost_per_t()[1]
col10 = NinhBinhSystem.transport_cost_per_t()[1]

assert isclose(col5 - col9, MongDuong1System.farmer.straw_value()[1] / col3)
assert isclose(col6 - col10, NinhBinhSystem.farmer.straw_value()[1] / col4)

print('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
print('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
print('{:24} {:>22.2f}{:>18.2f}'.format('Straw cost', col5, col6))
print('{:24} {:>22.2f}{:>18.2f}'.format('Biomass raw cost', col5 - col9, col6 - col10))
print('{:24} {:>19.2f}{:>18.2f}'.format('Biomass transportation cost', col9, col10))
print('')
print("Mong Duong", MongDuong1System.supply_chain)
print("Ninh Binh", NinhBinhSystem.supply_chain)
