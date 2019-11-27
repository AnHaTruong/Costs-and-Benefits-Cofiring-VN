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

from model.utils import solve_linear, USD, t


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

def plant_gain(system, biomass_price, discount_rate, tax_rate, depreciation_period):
    """Return plant's project profitability, for a given price of biomass."""
    original_price = system.price
    try:
        new_price = original_price._replace(biomass_plantgate=biomass_price)
        system.clear_market(new_price)
        npv_ante = system.plant.net_present_value(discount_rate, tax_rate, depreciation_period)
        npv_post = system.cofiring_plant.net_present_value(discount_rate,
                                                           tax_rate,
                                                           depreciation_period)
        profit = npv_post - npv_ante
    finally:
        system.clear_market(original_price)
    return profit


#%%

def plant_wtp(system, discount_rate, tax_rate, depreciation_period,
              starting_range=(0 * USD / t, 50 * USD / t)):
    """Compute and return the plant's willingness to pay for straw."""
    def gain(biomass_price):
        return plant_gain(system, biomass_price, discount_rate, tax_rate, depreciation_period)
    return solve_linear(gain, starting_range[0], starting_range[1])
