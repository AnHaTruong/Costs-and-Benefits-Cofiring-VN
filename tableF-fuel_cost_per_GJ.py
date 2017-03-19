# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Calculation of fuel cost per GJ"""

from parameters import MongDuong1Cofire, NinhBinhCofire
from parameters import MD_Coal, NB_Coal, straw


# Omitting coal transport costs ?

print("Cost of heat        MongDuong1          NinhBinh")
print("Coal               ", MD_Coal.cost_per_GJ(), "    ", NB_Coal.cost_per_GJ())
print("Biomass in field   ", straw.cost_per_GJ(), "    ", straw.cost_per_GJ())
print("Biomass plant gate ", MongDuong1Cofire.straw_supply.cost_per_GJ(straw.price, straw.heat_value)[1],
      "    ", NinhBinhCofire.straw_supply.cost_per_GJ(straw.price, straw.heat_value)[1])
