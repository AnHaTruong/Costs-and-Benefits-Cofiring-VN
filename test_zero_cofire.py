# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Test the boundary case: cofiring biomass ratio 0% is same as baseline plant."""

import pytest

from init import isclose, ZEROS
import parameters as baseline
from system import System
from powerplant import PowerPlant

# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name


@pytest.fixture()
def null_cofiring_system():
    return System(baseline.plant_parameter_MD1,
                  baseline.cofire_MD1._replace(biomass_ratio_energy=ZEROS),
                  baseline.SupplyChain_MD1,
                  baseline.price_MD1,
                  baseline.farm_parameter,
                  baseline.transport_parameter)


def test_npv(null_cofiring_system):
    npvA = null_cofiring_system.plant.net_present_value(0.08, 0.2, 10)
    npvB = null_cofiring_system.cofiring_plant.net_present_value(0.08, 0.2, 10)
    assert isclose(npvA, npvB)


def test_npv_powerplant(null_cofiring_system):
    p = PowerPlant(baseline.plant_parameter_MD1)
    p.revenue = p.power_generation * baseline.price_MD1.electricity
    p.coal_cost = p.coal_used * baseline.price_MD1.coal
    npvC = p.net_present_value(0.08, 0.2, 10)

    npvA = null_cofiring_system.plant.net_present_value(0.08, 0.2, 10)
    assert isclose(npvA, npvC)


def test_lcoe(null_cofiring_system):
    lcoeA = null_cofiring_system.plant.lcoe(0.08, 0.2, 10)
    lcoeB = null_cofiring_system.cofiring_plant.lcoe(0.08, 0.2, 10)
    assert isclose(lcoeA, lcoeB)
