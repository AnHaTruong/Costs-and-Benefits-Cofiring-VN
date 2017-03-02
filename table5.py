""" Print table 1 for Technical parameters of the plants"""

from parameters import MongDuong1Cofire, NinhBinhCofire

print("""
Table 5. Straw required and straw cost estimation
""")

col3 = MongDuong1Cofire.biomass_used[1]
col4 = NinhBinhCofire.biomass_used[1]

col5 = MongDuong1Cofire.biomass_cost_per_t()[1]
col6 = NinhBinhCofire.biomass_cost_per_t()[1]

col9 = MongDuong1Cofire.biomass_transport_cost_per_t()[1]
col10 = NinhBinhCofire.biomass_transport_cost_per_t()[1]

print('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
print('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
print('{:24} {:>22.2f}{:>18.2f}'.format('Straw cost', col5, col6))
print('{:24} {:>22.2f}{:>18.2f}'.format('Biomass raw cost', col5 - col9, col6 - col10))
print('{:24} {:>19.2f}{:>18.2f}'.format('Biomass transportation cost', col9, col10))
print('')
print("Mong Duong", MongDuong1Cofire.active_chain)
print("Ninh Binh", NinhBinhCofire.active_chain)
