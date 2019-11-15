# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Print the tables for manuscript 'Costs and benefits of co-firing'.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017-2019
"""

import pandas as pd
from natu.units import km, g, kg, t

from manuscript1.parameters import (MongDuong1System, NinhBinhSystem,
                                    emission_factor,
                                    discount_rate, tax_rate, depreciation_period,
                                    coal_import_price)
from model.utils import display_as


print('Parameters\n')

print('Time horizon          ', MongDuong1System.plant.parameter.time_horizon)
print('Discount rate         ', discount_rate)
print('Tax rate              ', tax_rate)
print('Depreciation period   ', depreciation_period)
print('Coal import price     ', display_as(coal_import_price, "USD/t"))

print('\nPower plants\n')

table = pd.concat(
    [MongDuong1System.plant.characteristics(),
     NinhBinhSystem.plant.characteristics()],
    axis=1)

pd.options.display.float_format = '{:,.2f}'.format

print(str(table))

print('\nEmission factors\n')

data = pd.DataFrame.from_dict(emission_factor).transpose()

table = pd.concat(
    [data.iloc[[0, 1, 7, 6]] / (kg / t),
     data.iloc[[4, 5]] / (g / (t * km))])

print(str(table))
