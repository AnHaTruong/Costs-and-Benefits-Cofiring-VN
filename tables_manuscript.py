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

from init import TIMEHORIZON

from parameters import MongDuong1System, NinhBinhSystem
from parameters import discount_rate, tax_rate, depreciation_period

from tables import emission_reductions, balance_jobs


systems = MongDuong1System, NinhBinhSystem

#%%

print('Table 1: Results of profitability assessment')
print("Net present value over", TIMEHORIZON, "years at discount rate =", discount_rate)
print("Tax rate", tax_rate, ", linear capital depreciation over ", depreciation_period, "years")
print()
df = pd.concat(
    [MongDuong1System.plant.lcoe_statement(discount_rate, tax_rate, depreciation_period),
     MongDuong1System.cofiring_plant.lcoe_statement(discount_rate, tax_rate, depreciation_period),
     NinhBinhSystem.plant.lcoe_statement(discount_rate, tax_rate, depreciation_period),
     NinhBinhSystem.cofiring_plant.lcoe_statement(discount_rate, tax_rate, depreciation_period)],
    axis=1)

pd.options.display.float_format = '{:,.1f}'.format
pd.set_option('display.width', 200)

print(str(df))


#%%

pd.options.display.float_format = '{:,.0f}'.format

table2 = """
Table 2: Emission reductions and associated benefits from the two projects

                    Mong Duong 1      Ninh Binh
""" + str(emission_reductions(MongDuong1System, NinhBinhSystem))

print(table2)

#%%

print("""
Table 3a: Supply chain earnings before taxes in the co-firing scenario.

Farmers             Mong Duong 1     Ninh Binh""")

df = pd.concat(
    [MongDuong1System.farmer.earning_before_tax_detail(),
     NinhBinhSystem.farmer.earning_before_tax_detail()],
    axis=1)

print(str(df))

print("""
Transporters        Mong Duong 1      Ninh Binh""")

df = pd.concat(
    [MongDuong1System.transporter.earning_before_tax_detail(),
     NinhBinhSystem.transporter.earning_before_tax_detail()],
    axis=1)

print(str(df))

#%%

print("""
Table 3b: Job creation and destruction in the co-firing scenario.

               Mong Duong 1  Ninh Binh""")

print(balance_jobs(*systems))


#%%
print("""
Table S1. Technical parameters
""")

df = pd.concat(
    [MongDuong1System.plant.characteristics(),
     NinhBinhSystem.plant.characteristics()],
    axis=1)

pd.options.display.float_format = '{:,.2f}'.format

print(str(df))
#%%
