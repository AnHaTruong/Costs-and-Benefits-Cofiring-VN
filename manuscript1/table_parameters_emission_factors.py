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

from manuscript1.parameters import emission_factor


data = pd.DataFrame.from_dict(emission_factor).transpose()

table = pd.concat(
    [data.iloc[[0, 1, 7, 6]] / (kg / t),
     data.iloc[[4, 5]] / (g / (t * km))])

print(table)
