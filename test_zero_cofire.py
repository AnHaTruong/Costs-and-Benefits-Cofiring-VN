# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Testing the boundary case: biomass ratio 0%
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
from natu.units import kWh
from init import USD, isclose, v_zeros
from parameters import MongDuong1, MD_SupplyChain, cofire_MD1
from PowerPlant import CofiringPlant

cofire_zero = cofire_MD1._replace(biomass_ratio_energy=v_zeros)

MongDuong1NullCofiring = CofiringPlant(MongDuong1, cofire_zero, supply_chain=MD_SupplyChain)

npvA = MongDuong1.net_present_value(1 * USD / kWh, 0.08, 0.2, 10)

npvB = MongDuong1NullCofiring.net_present_value(1 * USD / kWh, 0.08, 0.2, 10)

assert isclose(npvA, npvB)

lcoeA = MongDuong1.lcoe(1 * USD / kWh, 0.08, 0.2, 10)

lcoeB = MongDuong1NullCofiring.lcoe(1 * USD / kWh, 0.08, 0.2, 10)

assert isclose(npvA, npvB)
