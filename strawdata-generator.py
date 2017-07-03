# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Rice data processing
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
""" Assimilates rice production data into a Python valid format

We assume that within a province, the straw production is uniform
"""

import pandas as pd
from natu.units import ha, t
from natu.numpy import mean
from natu.math import fsum

# Leinonen and Nguyen 2013 : 50% of straw is collected and 79% of collected straw is sold
market_fraction = 0.5 * 0.79

residue_to_product_ratio = 1.0

df = pd.read_excel('Data/Rice_production_2014_GSO.xlsx', index_col=0)

df['straw yield'] = df['Rice yield (ton/ha)'] * residue_to_product_ratio * t / ha

df['straw density'] = (df['straw yield'] * df['Cultivation area (ha)'] * market_fraction
                       / df['Total area (ha)'])

df['straw production'] = df['rice production (ton)'] * residue_to_product_ratio * t


NinhBinh_straw_density = df.loc['Ninh Binh', 'straw density']
NinhBinh_straw_production = df.loc['Ninh Binh', 'straw production']
NinhBinh_average_straw_yield = df.loc['Ninh Binh', 'straw yield']


MongDuong1_straw_density1 = df.loc['Quang Ninh', 'straw density']

adjacent_provinces = ['Bac Giang', 'Hai Duong', 'Hai Phong']

size = {province: df.loc[province, 'Total area (ha)']
        for province in adjacent_provinces}

MongDuong1_straw_density2 = fsum([df.loc[province, 'straw density'] * size[province]
                                  for province in adjacent_provinces]) / sum(size.values())

all_provinces = adjacent_provinces + ['Quang Ninh']

MongDuong1_straw_production = fsum([df.loc[province, 'straw production']
                                    for province in all_provinces])

size = {province: df.loc[province, 'Total area (ha)']
        for province in all_provinces}

MongDuong1_average_straw_yield = fsum([df.loc[province, 'straw yield'] * size[province]
                                       for province in all_provinces]) / sum(size.values())


def line(q):
    """Returns the Python expression defining the value of quantity  q
    this expression is string litteral, to be saved for later evaluation
    can be imported by another file
    in base 10, as many significant digits as Python wants to print

    >>> test_qty = 2 * t
    >>> line("test_qty")
    'test_qty = 2 * t'

    I consider it a bug in  natu  that repr(q) omits the  *  between number and unit
    The  # nosec  comment disables bandit warning about using eval
    """
    valid_repr = repr(eval(q)).replace(' ', ' * ', 1)  # nosec
    return q + ' = ' + valid_repr


print("""
# This file automatically generated, DO NOT EDIT

from natu.units import t, ha
""",
      line("MongDuong1_straw_density1"),
      line("MongDuong1_straw_density2"),
      line("MongDuong1_straw_production"),
      line("MongDuong1_average_straw_yield"),
      line("NinhBinh_straw_density"),
      line("NinhBinh_straw_production"),
      line("NinhBinh_average_straw_yield"),
      sep='\n'
      )
