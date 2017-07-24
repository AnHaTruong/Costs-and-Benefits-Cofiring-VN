# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Testing the boundary case: biomass ratio 0%
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
from init import isclose, v_zeros
from parameters import MongDuong1, cofire_MD1, straw, MD_SupplyChain, feedin_tariff
from parameters import emission_factor, farm_parameter, transport_parameter
from System import System

MongDuong1NullCofiringSystem = System(MongDuong1,
                                      cofire_MD1._replace(biomass_ratio_energy=v_zeros),
                                      feedin_tariff["MD1"],
                                      MD_SupplyChain,
                                      straw.price,
                                      emission_factor,
                                      farm_parameter,
                                      transport_parameter)

MongDuong1NullCofiring = MongDuong1NullCofiringSystem.cofiring_plant

npvA = MongDuong1NullCofiring.plant.net_present_value(0.08, 0.2, 10)
npvB = MongDuong1NullCofiring.net_present_value(0.08, 0.2, 10)

#print("No cofiring NPV:", npvA)
#print("Cofiring 0% NPV:", npvB)

assert isclose(npvA, npvB)

lcoeA = MongDuong1NullCofiring.plant.lcoe(0.08, 0.2, 10)

lcoeB = MongDuong1NullCofiring.lcoe(0.08, 0.2, 10)

#print("No cofiring LCOE:", lcoeA)
#print("Cofiring 0% LCOE:", lcoeB)

assert isclose(lcoeA, lcoeB)
