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

from model.utils import display_as, USD, t

from model.wtawtp import farmer_wta, plant_wtp
from manuscript1.parameters import MongDuong1System, NinhBinhSystem
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period


def feasibility(system):
    """Determine the economic feasibility of cofiring."""
    wta = farmer_wta(system)
    display_as(wta, "USD/t")
    wtp = plant_wtp(system, discount_rate, tax_rate, depreciation_period)
    display_as(wtp, "USD/t")
    transport_cost = system.transport_cost_per_t[1]
    display_as(transport_cost, "USD/t")
    potential_gain = wtp - wta - transport_cost
    display_as(potential_gain, "USD/t")
    total_potential = potential_gain * system.cofiring_plant.biomass_used[1]
    display_as(total_potential, "kUSD")

    print(system.plant.parameter.name)
    print("WTP = ", wtp)
    print("WTA = ", wta)
    print("WTP - WTA = ", wtp - wta)
    print("Transport cost = ", transport_cost)
    print("Potential gain = ", potential_gain)
    print("Total potential = ", total_potential)

    return potential_gain > 0 * USD / t


feasibility(MongDuong1System)

print()
feasibility(NinhBinhSystem)
