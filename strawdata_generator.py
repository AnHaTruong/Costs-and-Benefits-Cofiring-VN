# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Rice data processing
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Assimilate rice production data into a Python valid format.

Assume that within a province, the straw production is uniform.
"""

import pandas as pd
from natu.units import ha, t
from natu.math import fsum

# Leinonen and Nguyen 2013 : 50% of straw is collected and 79% of collected straw is sold
market_fraction = 0.5 * 0.79

# Reference ???
residue_to_product_ratio = 1.0

df = pd.read_excel('Data/Rice_production_2014_GSO.xlsx', index_col=0)

df['straw yield'] = df['Rice yield (ton/ha)'] * residue_to_product_ratio * t / ha

df['straw density'] = (df['straw yield'] * df['Cultivation area (ha)'] * market_fraction
                       / df['Total area (ha)'])

df['straw production'] = df['rice production (ton)'] * residue_to_product_ratio * t

result = dict()

result['NinhBinh_straw_density'] = df.loc['Ninh Binh', 'straw density']
result['NinhBinh_straw_production'] = df.loc['Ninh Binh', 'straw production']
result['NinhBinh_average_straw_yield'] = df.loc['Ninh Binh', 'straw yield']


result['MongDuong1_straw_density1'] = df.loc['Quang Ninh', 'straw density']

adjacent_provinces = ['Bac Giang', 'Hai Duong', 'Hai Phong']

size = {province: df.loc[province, 'Total area (ha)']
        for province in adjacent_provinces}

result['MongDuong1_straw_density2'] = fsum(
    [df.loc[province, 'straw density'] * size[province]
     for province in adjacent_provinces]) / sum(size.values())

all_provinces = adjacent_provinces + ['Quang Ninh']

result['MongDuong1_straw_production'] = fsum(
    [df.loc[province, 'straw production']
     for province in all_provinces])

size = {province: df.loc[province, 'Total area (ha)']
        for province in all_provinces}

result['MongDuong1_average_straw_yield'] = fsum(
    [df.loc[province, 'straw yield'] * size[province]
     for province in all_provinces]) / sum(size.values())


def my_repr(quantity) -> str:
    """Return a valid Python representation of a quantity.

    Because the  Natu  bug with __repr__
    >>> m = 3 * t
    >>> str(m)
    '3 t'
    >>> repr(m)      # Should return '3 * t'
    '3 t'
    >>> my_repr(m)
    '3 * t'
    """
    return repr(quantity).replace(' t', ' * t', 1).replace('/ha', ' / ha', 1)


print('"""Automatically generated file, DO NOT EDIT."""')
print()
print('from natu.units import t, ha')
print()

for name, value in result.items():
    print(name, '=', my_repr(value))
