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
                  baseline.supply_chain_MD1,
                  baseline.price_MD1,
                  baseline.farm_parameter,
                  baseline.transport_parameter)


def test_npv(null_cofiring_system):
    npv_plant = null_cofiring_system.plant.net_present_value(0.08, 0.2, 10)
    npv_null_cofiring = null_cofiring_system.cofiring_plant.net_present_value(0.08, 0.2, 10)
    assert isclose(npv_plant, npv_null_cofiring)


def test_npv_powerplant(null_cofiring_system):
    plant = PowerPlant(baseline.plant_parameter_MD1)
    plant.revenue = plant.power_generation * baseline.price_MD1.electricity
    plant.coal_cost = plant.coal_used * baseline.price_MD1.coal
    npv_plant_direct = plant.net_present_value(0.08, 0.2, 10)

    npv_plant = null_cofiring_system.plant.net_present_value(0.08, 0.2, 10)
    assert isclose(npv_plant, npv_plant_direct)


def test_lcoe(null_cofiring_system):
    lcoe_plant = null_cofiring_system.plant.lcoe(0.08, 0.2, 10)
    lcoe_null_cofiring = null_cofiring_system.cofiring_plant.lcoe(0.08, 0.2, 10)
    assert isclose(lcoe_plant, lcoe_null_cofiring)
