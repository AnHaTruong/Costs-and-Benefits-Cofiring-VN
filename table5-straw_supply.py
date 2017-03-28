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

from parameters import MongDuong1Cofire, NinhBinhCofire

print("\nTable 5. Straw required and straw cost estimation\n""")

col3 = MongDuong1Cofire.biomass_used[1]
col4 = NinhBinhCofire.biomass_used[1]

col5 = MongDuong1Cofire.straw_supply.cost_per_t(MongDuong1Cofire.biomass.price)[1]
col6 = NinhBinhCofire.straw_supply.cost_per_t(NinhBinhCofire.biomass.price)[1]

col9 = MongDuong1Cofire.straw_supply.transport_cost_per_t()[1]
col10 = NinhBinhCofire.straw_supply.transport_cost_per_t()[1]

print('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
print('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
print('{:24} {:>22.2f}{:>18.2f}'.format('Straw cost', col5, col6))
print('{:24} {:>22.2f}{:>18.2f}'.format('Biomass raw cost', col5 - col9, col6 - col10))
print('{:24} {:>19.2f}{:>18.2f}'.format('Biomass transportation cost', col9, col10))
print('')
print("Mong Duong", MongDuong1Cofire.straw_supply)
print("Ninh Binh", NinhBinhCofire.straw_supply)
