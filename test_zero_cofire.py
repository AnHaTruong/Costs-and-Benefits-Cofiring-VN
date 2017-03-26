# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Testing the boundary case: biomass ratio 0%
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
from natu.units import hr, kW, y, kWh
from init import USD, isclose
from parameters import MongDuong1, straw, boiler_efficiency_loss, MD_SupplyChain
from PowerPlant import CofiringPlant

MongDuong1NullCofiring = CofiringPlant(
    MongDuong1,
    0.0,
    capital_cost=50 * USD / kW,
    fix_om_cost=32.24 * USD / kW / y,
    variable_om_cost=0.006 * USD / (kW * hr),
    biomass=straw,
    boiler_efficiency_loss=boiler_efficiency_loss,
    supply_chain=MD_SupplyChain
)

npvA = MongDuong1.net_present_value(1 * USD / kWh, 0.08, 0.2, 10)

npvB = MongDuong1NullCofiring.net_present_value(1 * USD / kWh, 0.08, 0.2, 10)

assert isclose(npvA, npvB)

lcoeA = MongDuong1.lcoe(1 * USD / kWh, 0.08, 0.2, 10)

lcoeB = MongDuong1NullCofiring.lcoe(1 * USD / kWh, 0.08, 0.2, 10)

assert isclose(npvA, npvB)
