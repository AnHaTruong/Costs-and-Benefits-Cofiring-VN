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

from model.utils import display_as, isclose

from model.wtawtp import farmer_wta, plant_wtp

from manuscript1.parameters import (MongDuong1System,   # NinhBinhSystem,
                                    discount_rate, tax_rate, depreciation_period)


row_labels = [
    'Farmer WTA',
    'Reseller expenses',
    'Plant WTP',
    'Potential gain',
    'Biomass used per year',
    'Business value per year',
    'Biomass used total',
    'Business value of cofiring']


def feasibility_by_solving(system):
    """Tabulate the WTA and WTP, using the micro definition: call code solving Profit(p) == 0."""
    wta = farmer_wta(system)
    wtp = plant_wtp(system, discount_rate, tax_rate, depreciation_period)
    transport_cost = system.transport_cost_per_t[1]
    potential_gain = wtp - wta - transport_cost

    q_per_year = system.cofiring_plant.biomass_used[1]
    potential_per_year = potential_gain * q_per_year
    q = np.npv(discount_rate, system.farmer.quantity)
    business_value = potential_gain * q

    data = [
        display_as(wta, "USD/t"),
        display_as(transport_cost, "USD/t"),
        display_as(wtp, "USD/t"),
        display_as(potential_gain, "USD/t"),
        q_per_year,                  # Changing the display format has too many side effects
        display_as(potential_per_year, "kUSD"),
        q,                           # Changing the display format has too many side effects
        display_as(business_value, "kUSD")]

    return pd.Series(data, index=row_labels, name=system.plant.name + ' by solve')


def feasibility_direct(system):
    """Tabulate the feasibility, using the theoretical analysis."""
    npv_table = system.table_business_value(discount_rate)
    q = np.npv(discount_rate, system.farmer.quantity)

    wta = npv_table.loc['Farmer opex'] / q
    assert isclose(wta, farmer_wta(system))
    minimum_margin = npv_table.loc['Transporter opex'] / q
    assert isclose(minimum_margin, system.transport_cost_per_t[1])
    investment = npv_table.loc['Investment'] / q
    extra_OM = npv_table.loc['Extra O&M'] / q
    coal_saving = npv_table.loc['Value of coal saved'] / q
    wtp = coal_saving - extra_OM - investment
    # assert isclose(wtp, plant_wtp(system, discount_rate))
    value_per_t = wtp - wta - minimum_margin
    value = value_per_t * q
    q_per_year = system.cofiring_plant.biomass_used[1]
    assert isclose(q_per_year, system.farmer.quantity[1])
    potential_per_year = q_per_year * value_per_t

    data = [
        display_as(wta, "USD/t"),
        display_as(minimum_margin, "USD/t"),
        display_as(wtp, "USD/t"),
        display_as(value_per_t, 'USD/t'),
        q_per_year,
        display_as(potential_per_year, 'kUSD'),
        q,
        display_as(value, "kUSD")]

    return pd.Series(data, index=row_labels, name=system.plant.name + ' direct')


print(pd.concat([
    feasibility_by_solving(MongDuong1System),
    feasibility_direct(MongDuong1System)],
    axis=1))
