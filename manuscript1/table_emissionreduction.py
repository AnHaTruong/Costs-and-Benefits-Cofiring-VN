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
from model.tables import emission_reductions


pd.options.display.float_format = '{:,.0f}'.format

table = """Emission reductions and associated benefits from the two projects
(external cost SKC)

                    Mong Duong 1      Ninh Binh
""" + str(emission_reductions(MongDuong1System, NinhBinhSystem, external_cost))

print(table)