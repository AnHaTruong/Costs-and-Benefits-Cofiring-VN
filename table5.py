""" Print table 1 for Technical parameters of the plants"""

from biomassrequired import biomass_required
from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from biomasscost import bm_unit_cost, bm_transportation_cost, collection_radius


print('')
print('Table 5. Straw required and straw cost estimation\n')

print('------ OLD -----------')

col3 = biomass_required(MongDuong1)
col4 = biomass_required(NinhBinh)

col5 = bm_unit_cost(MongDuong1)
col6 = bm_unit_cost(NinhBinh)

col9 = bm_transportation_cost(MongDuong1) / biomass_required(MongDuong1)
col10 = bm_transportation_cost(NinhBinh) / biomass_required(NinhBinh)

col11 = collection_radius(MongDuong1)
col12 = collection_radius(NinhBinh)

print('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
print('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
print('{:24} {:>22.2f}{:>20.2f}'.format('Straw cost', col5, col6))
print('{:24} {:>19.2f}{:>20.2f}'.format('Biomass transportation cost', col9, col10))
print('{:24} {:>21.1f}{:>23.1f}'.format('Collection radius', col11, col12))

print('')
print('------ NEW -----------')

col3 = MongDuong1Cofire.biomass_used[1]
col4 = NinhBinhCofire.biomass_used[1]

col5 = MongDuong1Cofire.biomass_cost_per_t()[1]
col6 = NinhBinhCofire.biomass_cost_per_t()[1]

col9 = MongDuong1Cofire.biomass_transport_cost_per_t()[1]
col10 = NinhBinhCofire.biomass_transport_cost_per_t()[1]

col11 = collection_radius(MongDuong1)
col12 = collection_radius(NinhBinh)

print('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
print('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
print('{:24} {:>22.2f}{:>20.2f}'.format('Straw cost', col5, col6))
print('{:24} {:>19.2f}{:>20.2f}'.format('Biomass transportation cost', col9, col10))
print('{:24} {:>21.1f}{:>23.1f}'.format('Collection radius', col11, col12))
