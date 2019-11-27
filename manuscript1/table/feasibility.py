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

from model.utils import display_as

from model.wtawtp import farmer_wta, plant_wtp

from manuscript1.parameters import (MongDuong1System, NinhBinhSystem,
                                    discount_rate, tax_rate, depreciation_period)


def feasibility(system):
    """Tabulate the WTA and WTP."""
    wta = farmer_wta(system)
    wtp = plant_wtp(system, discount_rate, tax_rate, depreciation_period)
    transport_cost = system.transport_cost_per_t[1]
    potential_gain = wtp - wta - transport_cost
    total_potential = potential_gain * system.cofiring_plant.biomass_used[1]

    data = [
        display_as(wta, "USD/t"),
        display_as(wtp, "USD/t"),
        wtp - wta,
        display_as(transport_cost, "USD/t"),
        display_as(potential_gain, "USD/t"),
        display_as(total_potential, "kUSD")]

    index = ['Farmer WTA',
             'Plant WTP',
             'Maximum spread WTP - WTA',
             'Reseller expenses',
             'Potential gain',
             'Total business value']

    df = pd.DataFrame(data, index=index, columns=[system.plant.parameter.name])
    return df


table = pd.concat([feasibility(MongDuong1System), feasibility(NinhBinhSystem)], axis=1)

print(table)

print(MongDuong1System.table_business_value(discount_rate, tax_rate, depreciation_period))
