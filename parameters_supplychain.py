# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Rice data processing
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Define the supply chains, based on rice production data.

Assume that within a province, the straw production is uniform.
"""

import pandas as pd
from natu.units import ha, t, km
from natu.math import fsum

from supplychain import SupplyChain, SupplyZone
from shape import Semiannulus, Disk


# Leinonen and Nguyen 2013 : 50% of straw is collected and 79% of collected straw is sold
market_fraction = 0.5 * 0.79

# Reference ???
residue_to_product_ratio = 1.0

df = pd.read_excel('Data/Rice_production_2014_GSO.xlsx', index_col=0)

df['straw yield'] = df['Rice yield (ton/ha)'] * residue_to_product_ratio * t / ha

df['straw density'] = (df['straw yield'] * df['Cultivation area (ha)'] * market_fraction
                       / df['Total area (ha)'])

df['straw production'] = df['rice production (ton)'] * residue_to_product_ratio * t

#%%

supply_zone_NB = SupplyZone(shape=Disk(50 * km),
                            straw_density=df.loc['Ninh Binh', 'straw density'],
                            tortuosity_factor=1.5)

supply_chain_NB = SupplyChain(zones=[supply_zone_NB],
                              straw_production=df.loc['Ninh Binh', 'straw production'],
                              straw_burn_rate=0.9,
                              average_straw_yield=df.loc['Ninh Binh', 'straw yield'])


#%%

supply_zone_1_MD = SupplyZone(shape=Semiannulus(0 * km, 50 * km),
                              straw_density=df.loc['Quang Ninh', 'straw density'],
                              tortuosity_factor=1.5)


adjacent_provinces = ['Bac Giang', 'Hai Duong', 'Hai Phong']

area_adjacent = {province: df.loc[province, 'Total area (ha)']
                 for province in adjacent_provinces}

straw_density_around_MD = fsum(
    [df.loc[province, 'straw density'] * area_adjacent[province]
     for province in adjacent_provinces]) / sum(area_adjacent.values())

supply_zone_2_MD = SupplyZone(shape=Semiannulus(50 * km, 100 * km),
                              straw_density=straw_density_around_MD,
                              tortuosity_factor=1.5)


all_provinces = adjacent_provinces + ['Quang Ninh']

straw_production_MD = fsum(
    [df.loc[province, 'straw production']
     for province in all_provinces])

area_all = {province: df.loc[province, 'Total area (ha)']
            for province in all_provinces}

straw_yield_MD = fsum(
    [df.loc[province, 'straw yield'] * area_all[province]
     for province in all_provinces]) / sum(area_all.values())


supply_chain_MD1 = SupplyChain(zones=[supply_zone_1_MD, supply_zone_2_MD],
                               straw_production=straw_production_MD,
                               straw_burn_rate=0.9,
                               average_straw_yield=straw_yield_MD)
