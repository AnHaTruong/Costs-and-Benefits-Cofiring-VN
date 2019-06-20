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
2017
"""

import pandas as pd

from manuscript1.parameters import (MongDuong1System, NinhBinhSystem,
                                    discount_rate, tax_rate, depreciation_period,
                                    external_cost, external_cost_SKC, external_cost_ZWY,
                                    external_cost_HAS)

from model.tables import (emission_reductions, balance_jobs,
                          emission_reductions_by_activity, emission_reductions_benefits)
from model.utils import display_as


table_separator = '\n=================\n'

#%%

pd.options.display.float_format = '{:,.1f}'.format

table1 = """
ICERE 2018 Table 1: Emission reductions by activity

""" + str(emission_reductions_by_activity(MongDuong1System, NinhBinhSystem, external_cost))

print(table1)


#%%
print(table_separator)

table2 = (
    "ICERE 2018 Table 2: Emission reductions benefits (external costs SKC, ZWY, HAS)\n\n" +
    "       Mong Duong 1                 Ninh Binh" +
    str(emission_reductions_benefits(MongDuong1System, NinhBinhSystem, external_cost_SKC)) +
    "\n\n" +
    str(emission_reductions_benefits(MongDuong1System, NinhBinhSystem, external_cost_ZWY)) +
    "\n\n" +
    str(emission_reductions_benefits(MongDuong1System, NinhBinhSystem, external_cost_HAS))
)

print(table2)


#%%
print(table_separator)

print('Table 1: Results of profitability assessment')
print("Net present value over", MongDuong1System.plant.parameter.time_horizon,
      "years at discount rate =", discount_rate)
print("Tax rate", tax_rate, ", linear capital depreciation over ", depreciation_period, "years")
print("Coal", MongDuong1System.price.coal, ", straw", MongDuong1System.price.biomass_plantgate)
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
print(table_separator)

pd.options.display.float_format = '{:,.0f}'.format

table2 = """Table 2: Emission reductions and associated benefits from the two projects

                    Mong Duong 1      Ninh Binh
""" + str(emission_reductions(MongDuong1System, NinhBinhSystem, external_cost))

print(table2)

#%%
print(table_separator)


def label(price):
    """Return a string with the straw price at field side and plant gate."""
    display_as(price.biomass_plantgate, 'USD/t')
    display_as(price.biomass_fieldside, 'USD/t')
    display_as(price.coal, 'USD/t')
    return ('Straw ' + str(price.biomass_fieldside) + ' field side, ' +
            str(price.biomass_plantgate) + ' plant gate')


print('Table 3a: Supply chain earnings before taxes in the co-firing scenario.')
print(label(NinhBinhSystem.price) + " in Ninh Binh")
print(label(MongDuong1System.price) + " in Mong Duong")
print()
print('Farmers             Mong Duong 1     Ninh Binh')

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
print(table_separator)

print("""Table 3b: Job creation and destruction in the co-firing scenario.

               Mong Duong 1  Ninh Binh""")

print(balance_jobs(MongDuong1System, NinhBinhSystem))


#%%
print(table_separator)

print('Table S1. Technical parameters\n')

df = pd.concat(
    [MongDuong1System.plant.characteristics(),
     NinhBinhSystem.plant.characteristics()],
    axis=1)

pd.options.display.float_format = '{:,.2f}'.format

print(str(df))
#%%
