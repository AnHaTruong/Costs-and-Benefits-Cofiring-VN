# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Determines the extreme market prices.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017
"""

from init import display_as, solve_linear

from parameters import MongDuong1System, NinhBinhSystem, price_MD1
from parameters import discount_rate, tax_rate, depreciation_period

financials = discount_rate, tax_rate, depreciation_period
systems = MongDuong1System, NinhBinhSystem


#%%

def farmer_ebt(system, biomass_price):
    """Return farmer's Excess Before Taxes, for a given biomass price."""
    original_price = system.price
    try:
        system.clear_market(original_price._replace(biomass=biomass_price))
        ebt = system.farmer.earning_before_tax()[1]
    finally:
        system.clear_market(original_price)
    display_as(biomass_price, "USD/t")
    print("Biomass price", biomass_price, "   EBT", ebt)
    return ebt

#%%


def farmer_minimum(system):
    """Compute and return the farmer's willingness to accept for its straw."""
    def f(x):
        return farmer_ebt(system, x)
    return solve_linear(f, price_MD1.biomass, price_MD1.biomass / 2)


print("Farmers WTA for Mong Duong 1 = ", farmer_minimum(MongDuong1System))


print("Farmers WTA for Ninh Binh = ", farmer_minimum(NinhBinhSystem))

#%%


def plant_gain(system, biomass_price, transport_price):
    """Return plant's project profitability, for a given price of biomass and transport."""
    original_price = system.price
    try:
        new_price = original_price._replace(biomass=biomass_price, transport=transport_price)
        system.clear_market(new_price)
        npv_ante = system.plant.net_present_value(discount_rate, tax_rate, depreciation_period)
        npv_post = system.cofiring_plant.net_present_value(discount_rate,
                                                           tax_rate,
                                                           depreciation_period)
        profit = npv_post - npv_ante
    finally:
        system.clear_market(original_price)
    display_as(biomass_price, "USD/t")
    display_as(transport_price, "USD/t/km")
    print("Biomass price", biomass_price, "USD/t  ", "Transport price", transport_price, "USD/t  ")
    print("Profit", profit)
    return profit
