# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Determines the farmer's WTA and plant's WTP for straw.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017-2019
"""
from pandas import Series
from natu.numpy import npv
from model.utils import solve_linear, USD, t, display_as, isclose


#%%

def farmer_gain(system, biomass_price):
    """Return farmer's Excess Before Taxes, for a given biomass price."""
    original_price = system.price
    try:
        system.clear_market(original_price._replace(biomass_fieldside=biomass_price))
        gain = system.farmer.earning_before_tax()[1]
    finally:
        system.clear_market(original_price)
    return gain


#%%

def farmer_wta(system,
               starting_range=(0 * USD / t, 50 * USD / t)):
    """Compute and return the farmer's willingness to accept for its straw."""
    def gain(biomass_price):
        return farmer_gain(system, biomass_price)
    return solve_linear(gain, starting_range[0], starting_range[1])


#%%

def plant_gain(system, biomass_price, discount_rate):
    """Return plant's project profitability before taxes, for a given price of biomass."""
    original_price = system.price
    try:
        new_price = original_price._replace(biomass_plantgate=biomass_price)
        system.clear_market(new_price)
        npv_ante = system.plant.net_present_value(discount_rate, tax_rate=0, depreciation_period=1)
        npv_post = system.cofiring_plant.net_present_value(discount_rate,
                                                           tax_rate=0,
                                                           depreciation_period=1)
#       npv_ante = npv(discount_rate, system.plant.earning_before_tax(depreciation_period))
#       npv_post = npv(discount_rate, system.cofiring_plant.earning_before_tax(depreciation_period))

        profit = npv_post - npv_ante
    finally:
        system.clear_market(original_price)
    return profit


#%%

def plant_wtp(system, discount_rate,
              starting_range=(0 * USD / t, 50 * USD / t)):
    """Compute and return the plant's willingness to pay for straw."""
    def gain(biomass_price):
        return plant_gain(system, biomass_price, discount_rate)
    return solve_linear(gain, starting_range[0], starting_range[1])


#%%

row_labels = [
    'Farmer WTA',
    'Reseller expenses',
    'Plant WTP',
    'Potential gain',
    'Biomass used total',
    'Business value of cofiring',
    'Biomass used per year',
    'Business value per year']


def feasibility_by_solving(system, discount_rate):
    """Tabulate the WTA and WTP, using the micro definition: call code solving Profit(p) == 0."""
    wta = farmer_wta(system)
    wtp = plant_wtp(system, discount_rate)
    transport_cost = system.transport_cost_per_t[1]
    potential_gain = wtp - wta - transport_cost
    q = npv(discount_rate, system.farmer.quantity)
    business_value = potential_gain * q

    q_per_year = system.cofiring_plant.biomass_used[1]
    potential_per_year = potential_gain * q_per_year

    data = [
        display_as(wta, "USD/t"),
        display_as(transport_cost, "USD/t"),
        display_as(wtp, "USD/t"),
        display_as(potential_gain, "USD/t"),
        q,                           # Changing the display format has too many side effects
        display_as(business_value, "kUSD"),
        q_per_year,                  # Changing the display format has too many side effects
        display_as(potential_per_year, "kUSD")]

    return Series(data, index=row_labels, name=system.plant.name + ' by solve')


def feasibility_direct(system, discount_rate):
    """Tabulate the feasibility, using the theoretical analysis."""
    npv_table = system.table_business_value(discount_rate)
    q = npv(discount_rate, system.farmer.quantity)

    wta = npv_table.loc['Farmer opex'] / q
    assert isclose(wta, farmer_wta(system))
    minimum_margin = npv_table.loc['Reseller opex'] / q
    assert isclose(minimum_margin, system.transport_cost_per_t[1])
    investment = npv_table.loc['Investment'] / q
    extra_OM = npv_table.loc['Extra O&M'] / q
    coal_saving = npv_table.loc['Value of coal saved'] / q
    wtp = coal_saving - extra_OM - investment
    assert isclose(wtp, plant_wtp(system, discount_rate))

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
        q,
        display_as(value, "kUSD"),
        q_per_year,
        display_as(potential_per_year, 'kUSD')]

    return Series(data, index=row_labels, name=system.plant.name + ' direct')
