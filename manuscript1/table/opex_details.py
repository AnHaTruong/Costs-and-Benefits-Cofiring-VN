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
from pandas import concat, set_option
from manuscript1.parameters import (
    MongDuong1System,
    NinhBinhSystem,
    discount_rate,
    tax_rate,
    depreciation_period,
    price_MD1,
    price_NB,
)

from model.utils import display_as


print("Business value of cofiring for the three segments")
print("Change in cash flow NPV,  ex post - ex ante")
# ex ante is zero for farmer and transpotrer segment
print(f"NPV at discount rate {100 * discount_rate}% per year")
print(f"Over {MongDuong1System.plant.time_horizon} years")
print()

p1MD1 = display_as(price_MD1.biomass_fieldside, "USD/t")
p1NB = display_as(price_NB.biomass_fieldside, "USD/t")
p2MD1 = display_as(price_MD1.biomass_plantgate, "USD/t")
p2NB = display_as(price_NB.biomass_plantgate, "USD/t")
print("Straw prices   Mong Duong 1   Ninh Binh")
print(f"p1             {p1MD1}         {p1NB}")
print(f"p2             {p2MD1}         {p2NB}")
print()

#%%


def result_table(systema_segment, systemb_segment):
    """Return a DataFrame with the NPV accounts of a segment in two systems."""
    table_a = systema_segment.npv_cash(discount_rate, tax_rate, depreciation_period)
    table_b = systemb_segment.npv_cash(discount_rate, tax_rate, depreciation_period)
    return concat([table_a, table_b], axis=1)


set_option("display.float_format", "{:,.0f} kUSD".format)

#%%
print("For farmers, the ex ante is null everywhere. Displaying only ex post:")
print(result_table(MongDuong1System.farmer, NinhBinhSystem.farmer))
print()
#%%
print("For reseller, the ex ante is null everywhere as well. Displaying only ex post:")
print(result_table(MongDuong1System.reseller, NinhBinhSystem.reseller))
print()
#%%
print("For power plant, the ex ante is no cofiring:")
print(result_table(MongDuong1System.plant, NinhBinhSystem.plant))
print()
#%%
print("For power plant, the ex post is with cofiring:")
print(result_table(MongDuong1System.cofiring_plant, NinhBinhSystem.cofiring_plant))
print()
#%%
print("For power plant, the change in net cash flow NPV (expost - exante):")
table_i = MongDuong1System.plant_npv_cash_change(
    discount_rate, tax_rate, depreciation_period
)
table_j = NinhBinhSystem.plant_npv_cash_change(
    discount_rate, tax_rate, depreciation_period
)
print(concat([table_i, table_j], axis=1))
print()
#%%
print("For power plant, the change in the operating expenses line (expost - exante):")
table_i_details = MongDuong1System.plant_npv_opex_change(discount_rate)
table_j_details = NinhBinhSystem.plant_npv_opex_change(discount_rate)
print(concat([table_i_details, table_j_details], axis=1))
