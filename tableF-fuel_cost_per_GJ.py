# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Print fuel costs per GJ."""

from init import display_as

from parameters import MongDuong1System, NinhBinhSystem
from parameters import coal_6b, coal_4b, straw, price_MD1, price_NB


def energy_cost(price, fuel):
    """Return the cost per unit of energy contained in the fuel."""
    cost = price / fuel.heat_value
    return display_as(cost, 'USD / GJ')

print("Cost of heat        MongDuong1          NinhBinh")
print("Coal               ",                             # At plant gate
      energy_cost(price_MD1.coal, coal_6b), "    ",
      energy_cost(price_NB.coal, coal_4b))
print("Biomass in field   ",
      energy_cost(price_MD1.biomass, straw), "    ",
      energy_cost(price_NB.biomass, straw))
print("Biomass plant gate ",
      MongDuong1System.cofiring_plant.biomass_cost_per_GJ()[1],
      "    ", NinhBinhSystem.cofiring_plant.biomass_cost_per_GJ()[1])
