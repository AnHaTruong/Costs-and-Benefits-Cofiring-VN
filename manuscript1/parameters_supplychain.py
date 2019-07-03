# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Rice data processing
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Define the supply chains, based on rice production data.

Assume that within a province, the straw production is uniform.
"""

import pandas as pd
from natu.units import ha, t, km
from natu.math import fsum

from model.supplychain import SupplyChain, SupplyZone
from model.shape import Semiannulus, Disk


# Leinonen and Nguyen 2013 : 50% of straw is collected and 79% of collected straw is sold
_sold_fraction = 0.5 * 0.79
_residue_to_product_ratio = 1.0   # Reference ???
_tortuosity_factor = 1.5          # Reference ???

df = pd.read_excel('Data/Rice_production_2014_GSO.xlsx', index_col=0)

#%%

supply_zone_NB = SupplyZone(
    shape=Disk(50 * km),
    rice_yield_per_crop=df.loc['Ninh Binh', 'Rice yield (ton/ha)'] * t / ha,
    rice_land_fraction=(df.loc['Ninh Binh', 'Cultivation area (ha)'] /
                        df.loc['Ninh Binh', 'Total area (ha)']),
    straw_to_rice_ratio=_residue_to_product_ratio,
    tortuosity_factor=_tortuosity_factor,
    sold_fraction=_sold_fraction)

supply_chain_NB = SupplyChain(
    zones=[supply_zone_NB],
    straw_production=df.loc['Ninh Binh', 'rice production (ton)'] * _residue_to_product_ratio * t,
    average_straw_yield=(df.loc['Ninh Binh', 'Rice yield (ton/ha)'] * t / ha *
                         _residue_to_product_ratio))


#%%

supply_zone_1_MD = SupplyZone(
    shape=Semiannulus(0 * km, 50 * km),
    rice_yield_per_crop=df.loc['Quang Ninh', 'Rice yield (ton/ha)'] * t / ha,
    rice_land_fraction=(df.loc['Quang Ninh', 'Cultivation area (ha)'] /
                        df.loc['Quang Ninh', 'Total area (ha)']),
    straw_to_rice_ratio=_residue_to_product_ratio,
    tortuosity_factor=_tortuosity_factor,
    sold_fraction=_sold_fraction)


provinces_around = ['Bac Giang', 'Hai Duong', 'Hai Phong']

total_area_around_MD = fsum([
    df.loc[province, 'Total area (ha)']
    for province in provinces_around])

cultivation_area_around_MD = fsum([
    df.loc[province, 'Cultivation area (ha)']
    for province in provinces_around])

#  yield in the zone is a weighted average of yield in the provices
#  Yield is per crop, production is per year - and there are multiple crops per year.
#  So  yield * area  is not same as  production
rice_yield_around_MD = fsum([
    df.loc[province, 'Rice yield (ton/ha)'] *
    df.loc[province, 'Cultivation area (ha)'] / cultivation_area_around_MD
    for province in provinces_around])


supply_zone_2_MD = SupplyZone(
    shape=Semiannulus(50 * km, 100 * km),
    rice_yield_per_crop=rice_yield_around_MD * t / ha,
    rice_land_fraction=cultivation_area_around_MD / total_area_around_MD,
    straw_to_rice_ratio=_residue_to_product_ratio,
    tortuosity_factor=_tortuosity_factor,
    sold_fraction=_sold_fraction)


all_provinces = provinces_around + ['Quang Ninh']

straw_production_MD = fsum([
    df.loc[province, 'rice production (ton)'] * _residue_to_product_ratio * t
    for province in all_provinces])

area_all_MD = fsum([
    df.loc[province, 'Total area (ha)']
    for province in all_provinces])

straw_yield_MD = fsum([
    df.loc[province, 'Rice yield (ton/ha)'] * _residue_to_product_ratio * t / ha *
    df.loc[province, 'Total area (ha)']
    for province in all_provinces]) / area_all_MD


supply_chain_MD1 = SupplyChain(
    zones=[supply_zone_1_MD, supply_zone_2_MD],
    straw_production=straw_production_MD,
    average_straw_yield=straw_yield_MD)
