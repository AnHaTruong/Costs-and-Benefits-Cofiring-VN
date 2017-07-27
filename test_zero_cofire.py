# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Testing the boundary case: biomass ratio 0%"""

from init import isclose, v_zeros
from parameters import plant_parameter_MD1, cofire_MD1, SupplyChain_MD1, price_MD1
from parameters import farm_parameter, transport_parameter
from System import System
from PowerPlant import PowerPlant

MongDuong1NullCofiringSystem = System(plant_parameter_MD1,
                                      cofire_MD1._replace(biomass_ratio_energy=v_zeros),
                                      SupplyChain_MD1,
                                      price_MD1,
                                      farm_parameter,
                                      transport_parameter)

npvA = MongDuong1NullCofiringSystem.plant.net_present_value(0.08, 0.2, 10)
npvB = MongDuong1NullCofiringSystem.cofiring_plant.net_present_value(0.08, 0.2, 10)

# print("No cofiring NPV:", npvA)
# print("Cofiring 0% NPV:", npvB)

assert isclose(npvA, npvB)

p = PowerPlant(plant_parameter_MD1)
p.revenue = p.power_generation * price_MD1.electricity
p.coal_cost = p.coal_used * price_MD1.coal
npvC = p.net_present_value(0.08, 0.2, 10)

# print("No cofiring NPV:", npvA)
# print("Direct PowerPlant object:", npvC)

assert isclose(npvA, npvC)

lcoeA = MongDuong1NullCofiringSystem.plant.lcoe(0.08, 0.2, 10)

lcoeB = MongDuong1NullCofiringSystem.cofiring_plant.lcoe(0.08, 0.2, 10)

# print("No cofiring LCOE:", lcoeA)
# print("Cofiring 0% LCOE:", lcoeB)

assert isclose(lcoeA, lcoeB)
