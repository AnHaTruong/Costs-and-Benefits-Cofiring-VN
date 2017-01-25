""" Print table 1 for Technical parameters of the plants"""

from biomassrequired import biomass_required
from parameters import MongDuong1, NinhBinh
from biomasscost import bm_unit_cost, bm_transportation_cost, collection_radius


print('')
print('Table 5. Straw require and straw cost estimation')

head = '{:24}'+' {:>20}'*2
row = '{:24}'+' {:>20}'*2


col1 = MongDuong1.electricity_tariff
col2 = NinhBinh.electricity_tariff
col1.display_unit = 'USD/kWh'
col2.display_unit = 'USD/kWh'

col3 = biomass_required(MongDuong1)
col4 = biomass_required(NinhBinh)
col3.display_unit = 't/y'
col4.display_unit = 't/y'

col5 = bm_unit_cost(MongDuong1)
col6 = bm_unit_cost(NinhBinh)
col5.display_unit = 'USD/t'
col6.display_unit = 'USD/t'

col7 = MongDuong1.coal_price
col8 = NinhBinh.coal_price
col7.display_unit = 'USD/t'
col8.display_unit = 'USD/t'

col9 = bm_transportation_cost(MongDuong1) / biomass_required(MongDuong1)
col10 = bm_transportation_cost(NinhBinh) / biomass_required(NinhBinh)
col9.display_unit = 'USD/t'
col10.display_unit = 'USD/t'

col11 = collection_radius(MongDuong1)
col12 = collection_radius(NinhBinh)
col11.display_unit = 'km'
col12.display_unit = 'km'

print(head.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))

print(row.format('Straw required', col3, col4))
print(row.format('Straw price', col5, col6))
print(row.format('Coal price',  col7, col8))
print(row.format('Electricity price',  col1, col2))
print(row.format('Biomass transportation cost', col9, col10))
print(row.format('Collection radius', col11, col12))
