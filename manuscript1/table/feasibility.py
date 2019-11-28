# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Determines the extreme market prices.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017
"""
import pandas as pd
import natu.numpy as np

from model.utils import display_as

from model.wtawtp import farmer_wta, plant_wtp

from manuscript1.parameters import (MongDuong1System,   # NinhBinhSystem,
                                    discount_rate, tax_rate, depreciation_period)


def feasibility_by_solving(system):
    """Tabulate the WTA and WTP, using the micro definition: call code solving Profit(p) == 0."""
    wta = farmer_wta(system)
    wtp = plant_wtp(system, discount_rate, tax_rate, depreciation_period)
    transport_cost = system.transport_cost_per_t[1]
    potential_gain = wtp - wta - transport_cost
    q = system.cofiring_plant.biomass_used[1]
    total_potential = potential_gain * q

    data = [
        display_as(wta, "USD/t"),
        display_as(transport_cost, "USD/t"),
        display_as(wtp, "USD/t"),
        display_as(potential_gain, "USD/t"),
        q,
        display_as(total_potential, "MUSD")]

    index = ['Farmer WTA',
             'Reseller expenses',
             'Plant WTP',
             'Potential gain',
             'Biomass used',
             'Total business value']

    return pd.Series(data, index=index, name=system.plant.name + ' by solving')


def feasibility_direct(system):
    """Tabulate the feasibility, using the theoretical analysis."""
    npv_table = system.table_business_value(discount_rate)

    q = np.npv(discount_rate, system.farmer.quantity)

    wta = npv_table.loc['Farmer opex'] / q
    display_as(wta, "USD/t")

    minimum_margin = npv_table.loc['Transporter opex'] / q
    display_as(minimum_margin, "USD/t")

    investment = npv_table.loc['Investment'] / q
    extra_OM = npv_table.loc['Extra O&M'] / q
    coal_saving = npv_table.loc['Value of coal saved'] / q
    wtp = coal_saving - extra_OM - investment
    display_as(wtp, "USD/t")

    value_per_t = wtp - wta - minimum_margin

    value = value_per_t * q
    display_as(value, "MUSD")

    table = pd.Series(
        data=[wta, minimum_margin, wtp, value_per_t, q, value],
        index=["Farmer WTA",
               "Reseller expenses",
               "Plant WTP",
               "Potential gain",
               "Biomass used",
               "Total business value"])
    table.name = system.plant.name + " Direct"
    return table


print(pd.concat([
    feasibility_by_solving(MongDuong1System),
    feasibility_direct(MongDuong1System)],
    axis=1))
