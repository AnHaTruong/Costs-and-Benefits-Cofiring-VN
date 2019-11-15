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

from model.utils import display_as, solve_linear, USD, t

from manuscript1.parameters import MongDuong1System, NinhBinhSystem, price_MD1
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period

financials = discount_rate, tax_rate, depreciation_period
systems = MongDuong1System, NinhBinhSystem


#%%

def farmer_ebt(system, biomass_price):
    """Return farmer's Excess Before Taxes, for a given biomass price."""
    original_price = system.price
    try:
        system.clear_market(original_price._replace(biomass_fieldside=biomass_price))
        ebt = system.farmer.earning_before_tax()[1]
    finally:
        system.clear_market(original_price)
#    display_as(biomass_price, "USD/t")
#    print("Biomass price", biomass_price, "   EBT", ebt)
    return ebt

#%%


def farmer_minimum(system):
    """Compute and return the farmer's willingness to accept for its straw."""
    def f(x):
        return farmer_ebt(system, x)
    return solve_linear(f, price_MD1.biomass_fieldside, price_MD1.biomass_fieldside / 2)


#%%


def plant_gain(system, biomass_price):
    """Return plant's project profitability, for a given price of biomass.

    Transport cost should not matter.
    """
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
#    display_as(biomass_price, "USD/t")
#    print("Biomass price", biomass_price, "    ", "Profit", profit)
    return profit


def plant_maximum(system):
    """Compute and return the plant's willingness to pay for straw."""
    def f(x):
        return plant_gain(system, x)
    return solve_linear(f, price_MD1.biomass_plantgate, price_MD1.biomass_plantgate / 2)


def feasibility(system):
    """Determine the economic feasibility of cofiring."""
    wta = farmer_minimum(system)
    display_as(wta, "USD/t")
    wtp = plant_maximum(system)
    display_as(wtp, "USD/t")
    transport_cost = system.transport_cost_per_t[1]
    display_as(transport_cost, "USD/t")
    potential_gain = wtp - wta - transport_cost
    display_as(potential_gain, "USD/t")
    total_potential = potential_gain * system.cofiring_plant.biomass_used[1]
    display_as(total_potential, "kUSD")

    print("WTP = ", wtp)
    print("WTA = ", wta)
    print("WTP - WTA = ", wtp - wta)
    print("Transport cost = ", transport_cost)
    print("Potential gain = ", potential_gain)
    print("Total potential = ", total_potential)

    return potential_gain > 0 * USD / t


print("Mong Duong 1")
feasibility(MongDuong1System)

print()
print("Ninh Binh")
feasibility(NinhBinhSystem)
