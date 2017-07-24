# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Calculation of fuel cost per GJ"""

from init import display_as

from parameters import MongDuong1System, NinhBinhSystem
from parameters import coal_6b, coal_4b, straw, price_MD1, price_NB


def cost_per_GJ(price, fuel):
    cost = price / fuel.heat_value
    return display_as(cost, 'USD / GJ')


# Omitting coal transport costs ?

print("Cost of heat        MongDuong1          NinhBinh")
print("Coal               ",
      cost_per_GJ(price_MD1.coal, coal_6b), "    ",
      cost_per_GJ(price_NB.coal, coal_4b))
print("Biomass in field   ",
      cost_per_GJ(price_MD1.biomass, straw), "    ",
      cost_per_GJ(price_NB.biomass, straw))
print("Biomass plant gate ",
      MongDuong1System.cofiring_plant.biomass_cost_per_GJ()[1],
      "    ", NinhBinhSystem.cofiring_plant.biomass_cost_per_GJ()[1])
