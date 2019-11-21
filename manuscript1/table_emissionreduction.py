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

from manuscript1.parameters import MongDuong1System, NinhBinhSystem, external_cost
from model.tables import emissions_reduction_ICERE


pd.options.display.float_format = '{:,.0f}'.format

table = """Emission reductions from the two projects

                    Mong Duong 1      Ninh Binh
""" + str(emissions_reduction_ICERE(MongDuong1System, NinhBinhSystem, external_cost))

print(table)
