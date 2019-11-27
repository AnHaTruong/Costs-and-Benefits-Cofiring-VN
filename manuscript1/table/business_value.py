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
import natu.numpy as np

from manuscript1.parameters import (MongDuong1System, NinhBinhSystem, discount_rate,
                                    price_MD1, price_NB)

from model.utils import display_as, kUSD


print("Business value of cofiring for the three segments")
print("Change in cash flow NPV,  ex post - ex ante")
#ex ante is zero for farmer and transpotrer segment
print(f"NPV at discount rate {100 * discount_rate}% per year")
print(f"Over {MongDuong1System.plant.time_horizon} years")
print()

p1MD1 = display_as(price_MD1.biomass_fieldside, "USD/t")
p1NB = display_as(price_NB.biomass_fieldside, "USD/t")
p2MD1 = display_as(price_MD1.biomass_plantgate, "USD/t")
p2NB = display_as(price_NB.biomass_plantgate, "USD/t")
print(f"Straw prices   Mong Duong 1   Ninh Binh")
print(f"p1             {p1MD1}         {p1NB}")
print(f"p2             {p2MD1}         {p2NB}")
print()

#%%


def result(system_segment, name):
    """Tabulate the effects of cofiring on stakeholder's NPV."""
    cash_result = system_segment.business_data()[1]
    data = cash_result.apply((lambda x: np.npv(discount_rate, x)), axis=1)
    df = pd.DataFrame(data)
    df.columns = [name]
    return df


pd.options.display.float_format = '{:,.0f} kUSD'.format

#%%

table_a = result(MongDuong1System.farmer, "MD1 farmer")
table_b = result(NinhBinhSystem.farmer, 'NB farmer')
print(pd.concat([table_a, table_b], axis=1))
print()

#%%

table_c = result(MongDuong1System.transporter, "MD1 reseller")
table_d = result(NinhBinhSystem.transporter, 'NB reseller')
print(pd.concat([table_c, table_d], axis=1))
print()

#%%

table_e = result(MongDuong1System.cofiring_plant, "MD1 cofiring plant")
table_f = result(NinhBinhSystem.cofiring_plant, 'NB cofiring plant')
# print(pd.concat([table_e, table_f], axis=1))

#%%

table_g = result(MongDuong1System.plant, "MD1 plant")
table_h = result(NinhBinhSystem.plant, 'NB plant')
# print(pd.concat([table_g, table_h], axis=1))

#%%


def plant_cash_change(system):
    """Return the cofiring project evaluation NPV tables, table that detail OPEX."""
    _, cash_exante, opex_exante = system.plant.business_data()
    _, cash_expost, opex_expost = system.cofiring_plant.business_data()
    npv_exante = cash_exante.apply((lambda x: np.npv(discount_rate, x)), axis=1)
    npv_expost = cash_expost.apply((lambda x: np.npv(discount_rate, x)), axis=1)
    df = pd.DataFrame(npv_expost - npv_exante)
    df.columns = [system.plant.name]

    npv_opex_exante = opex_exante.apply((lambda x: np.npv(discount_rate, x)), axis=1)
    npv_opex_expost = opex_expost.apply((lambda x: np.npv(discount_rate, x)), axis=1)
    df_opex = pd.DataFrame(npv_opex_expost)
    df_opex.loc['Fuel cost, coal'] -= npv_opex_exante.loc['Fuel cost, coal']
    df_opex.loc['O&M, coal'] -= npv_opex_exante.loc['Operation & Maintenance']
    df_opex.loc['= Operating expenses (kUSD)'] -= npv_opex_exante.loc['= Operating expenses (kUSD)']
    df_opex.columns = [system.plant.name]
    return df, df_opex


table_i, table_i_details = plant_cash_change(MongDuong1System)
table_j, table_j_details = plant_cash_change(NinhBinhSystem)

print(pd.concat([table_i, table_j], axis=1))
print()

print(pd.concat([table_i_details, table_j_details], axis=1))
print()

#%%


def table_business_value(system):
    """Tabulate cofiring business value:  technical costs vs. value of coal saved."""
    data = [
        np.npv(discount_rate, system.farmer.operating_expenses()),
        np.npv(discount_rate, system.transporter.operating_expenses()),
        np.npv(discount_rate, system.cofiring_plant.investment())]

    df, df_opex = plant_cash_change(system)
    extra_OM = df_opex.loc['O&M, coal'] + df_opex.loc['O&M, biomass']
    data.append(display_as(extra_OM[0] * kUSD, 'kUSD'))

    technical_cost = np.sum(data)
    data.append(technical_cost)

    coal_saved = np.npv(discount_rate, system.coal_saved)
    coal_price = display_as(system.price.coal, "USD/t")
    savings = display_as(coal_saved * coal_price, "kUSD")
    data.append(coal_saved)
    data.append(coal_price)
    data.append(savings)

    data.append(savings - technical_cost)

    index = [
        "Farmer opex",
        "Transporter opex",
        "Investment",
        "Extra O&M",
        "Total technical costs",
        "Coal saved",
        "Coal price",
        "Value of coal saved",
        "Business value of cofiring"]
    df = pd.DataFrame(data, index=index)
    df.columns = [system.plant.name]
    return df


table_k = table_business_value(MongDuong1System)
table_l = table_business_value(NinhBinhSystem)

print(pd.concat([table_k, table_l], axis=1))