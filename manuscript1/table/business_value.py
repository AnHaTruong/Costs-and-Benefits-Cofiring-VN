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
from pandas import concat

from model.utils import display_as
from model.wtawtp import feasibility_direct

from manuscript1.parameters import (
    MongDuong1System,
    NinhBinhSystem,
    discount_rate,
    economic_horizon,
    depreciation_period,
    farm_parameter,
)

print("Submitted manuscript discounts at rate 0.1 per year over 21 years.")
print("In revision use the tables with discount (0%) over 10 years.")
print("Also suggest to drop ros Business value per year since already in Figure 5")
print()

#%%

print("Business value of cofiring, from project NPVs.\n")
print("Discounted at", discount_rate, "over", economic_horizon, "years")
print(
    concat(
        [
            MongDuong1System.table_business_value(discount_rate, economic_horizon),
            NinhBinhSystem.table_business_value(discount_rate, economic_horizon),
        ],
        axis=1,
    )
)

print("\n")
print("Discounted at", 0, "over", depreciation_period, "years")
print(
    concat(
        [
            MongDuong1System.table_business_value(0, depreciation_period),
            NinhBinhSystem.table_business_value(0, depreciation_period),
        ],
        axis=1,
    )
)

#%%

print("\n")
print("Business value of cofiring, from WTA, WTP and other per t values.\n")
print("Discounted at", discount_rate, "over", economic_horizon, "years")
table_MD1 = feasibility_direct(MongDuong1System, discount_rate, economic_horizon)
table_NB = feasibility_direct(NinhBinhSystem, discount_rate, economic_horizon)

print(concat([table_MD1, table_NB], axis=1))


print("\n")
print("Business value of cofiring, from WTA, WTP and other per t values.\n")
print("Discounted at", 0, "over", depreciation_period, "years")
table_MD1 = feasibility_direct(MongDuong1System, 0, depreciation_period)
table_NB = feasibility_direct(NinhBinhSystem, 0, depreciation_period)

print(concat([table_MD1, table_NB], axis=1))

#%%

print("\n")
print("Relative economic importance.")

MD1_revenue = MongDuong1System.plant.revenue[0]
NB_revenue = NinhBinhSystem.plant.revenue[0]

print("")
print("Income from electricity sales.")
print("Mong Duong 1:  ", MD1_revenue, "per year")
print("NInh Binh   :  ", NB_revenue, "per year")

MD1_value = table_MD1.loc["Business value per year"]
NB_value = table_NB.loc["Business value per year"]

print("")
print("Business value of cofiring per year / Income from electricity sales per year.")
print("Mong Duong 1:  {:.1f}%".format(100 * MD1_value / MD1_revenue))
print("NInh Binh   :  {:.1f}%".format(100 * NB_value / NB_revenue))

#%%

MD1_rice_area = display_as(MongDuong1System.supply_chain.ricegrowing_area(), "ha")
NB_rice_area = display_as(NinhBinhSystem.supply_chain.ricegrowing_area(), "ha")

print("")
print("Rice growing areas.")
print("Mong Duong 1:  ", MD1_rice_area)
print("NInh Binh   :  ", NB_rice_area)

MD1_value_per_ha = display_as(
    table_MD1.loc["Business value per year"] / MD1_rice_area, "USD/ha"
)
NB_value_per_ha = display_as(
    table_NB.loc["Business value per year"] / NB_rice_area, "USD/ha"
)

print("")
print("Business value of cofiring per ha per year.")
print("Mong Duong 1:  {:.2f}".format(MD1_value_per_ha))
print("NInh Binh   :  {:.2f}".format(NB_value_per_ha))


print("")
print("Business value of cofiring per ha per year / farming profit.")
print("Mong Duong 1:  {:.1f}%".format(100 * MD1_value_per_ha / farm_parameter.profit))
print("NInh Binh   :  {:.1f}%".format(100 * NB_value_per_ha / farm_parameter.profit))
