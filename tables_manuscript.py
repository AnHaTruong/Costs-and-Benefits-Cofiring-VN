# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Print the tables for manuscript 'Costs and benefits of co-firing'.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017
"""

import pandas as pd

from parameters import MongDuong1System, NinhBinhSystem
from tables import lcoe, technical_parameters, emission_reductions
from tables import balance_sheet_farmer, balance_sheet_transporter, balance_jobs


systems = MongDuong1System, NinhBinhSystem

#%%

print('Table 1: Results of profitability assessment')

print(lcoe(MongDuong1System))
print(lcoe(NinhBinhSystem))

#%%

pd.options.display.float_format = '{:,.0f}'.format


table2 = """
Table 2: Emission reductions and associated benefit from two plants

                    Mong Duong 1      Ninh Binh
""" + str(emission_reductions(MongDuong1System, NinhBinhSystem))

print(table2)

#%%

print("""
Table 3a: Supply chain income and expenses in the co-firing scenario.

Farmers             Mong Duong 1      Ninh Binh""")

print(balance_sheet_farmer(*systems))

print("""
Transporters        Mong Duong 1      Ninh Binh""")

print(balance_sheet_transporter(*systems))

#%%

print("""
Table 3b: Job creation and destruction in the co-firing scenario.

               Mong Duong 1  Ninh Binh""")

print(balance_jobs(*systems))


#%%
print("""
Table S1. Technical parameters
""")

print(technical_parameters(MongDuong1System, NinhBinhSystem))

#%%
