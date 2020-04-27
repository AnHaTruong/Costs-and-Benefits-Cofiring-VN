# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Regression testing. Did results change?"""


import pytest

from pandas import set_option

# pylint: disable=wrong-import-position
from natu import config

config.use_quantities = False

from manuscript1.parameters import MongDuong1System, NinhBinhSystem
from manuscript1.parameters import discount_rate, tax_rate, depreciation_period
from manuscript1.parameters import external_cost, coal_import_price, mining_parameter
from model.tables import (
    energy_costs,
    straw_supply,
    emissions_reduction_benefit,
    emissions_reduction_ICERE,
    business_value_by_solving,
    business_value_direct,
)


# Quiet unused-import warning from pylint and spyder, we use them inside an eval string
_ = coal_import_price, mining_parameter

# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name

set_option("display.max_columns", None)
set_option("display.width", 10000)
set_option("display.float_format", "{:,.1f}".format)

finance = discount_rate, tax_rate, depreciation_period


@pytest.fixture()
def systems():
    return MongDuong1System, NinhBinhSystem


def test_energy_costs(regtest, systems):
    regtest.write(energy_costs(*systems))


def test_emissions_reduction_benefit(regtest, systems):
    regtest.write(
        str(emissions_reduction_benefit(*systems, external_cost, discount_rate))
    )


def test_emission_reductions(regtest, systems):
    regtest.write(str(emissions_reduction_ICERE(*systems, external_cost)))


def test_straw_supply(regtest, systems):
    regtest.write(straw_supply(*systems))


def test_business_value_by_solving(regtest, systems):
    regtest.write(str(business_value_by_solving(*systems, discount_rate)))


def test_business_value_direct(regtest, systems):
    regtest.write(str(business_value_direct(*systems, discount_rate)))


# pylint: disable=eval-used, unused-argument
def f(systems, method):
    result_a = eval("systems[0]." + method)
    result_b = eval("systems[1]." + method)
    return str(result_a) + "\n\n" + str(result_b)


def test_plant_lcoe_statement(regtest, systems):
    set_option("display.float_format", "{:9,.1f}".format)
    regtest.write(f(systems, "plant.lcoe_statement(*finance)"))


def test_cofiring_plant_lcoe(regtest, systems):
    set_option("display.float_format", "{:9,.1f}".format)
    regtest.write(f(systems, "cofiring_plant.lcoe_statement(*finance)"))


def test_technical_parameters(regtest, systems):
    set_option("display.float_format", "{:9,.2f}".format)
    regtest.write(f(systems, "plant.characteristics()"))


def test_emissions_baseline(regtest, systems):
    regtest.write(f(systems, "emissions_baseline()"))


def test_emissions_cofiring(regtest, systems):
    regtest.write(f(systems, "emissions_cofiring()"))


def test_plant_parameters(regtest, systems):
    regtest.write(f(systems, "plant.parameters_table()"))


def test_plant_business_data(regtest, systems):
    regtest.write(f(systems, "plant.business_data(tax_rate, depreciation_period)"))


def test_cofiring_parameters(regtest, systems):
    regtest.write(f(systems, "cofiring_plant.parameters_table()"))


def test_cofiring_business_data(regtest, systems):
    regtest.write(
        f(systems, "cofiring_plant.business_data(tax_rate, depreciation_period)")
    )


def test_farmer_parameters(regtest, systems):
    regtest.write(f(systems, "farmer.parameters_table()"))


def test_farmer_business_data(regtest, systems):
    regtest.write(f(systems, "farmer.business_data(tax_rate, depreciation_period)"))


def test_reseller_parameters(regtest, systems):
    regtest.write(f(systems, "reseller.parameters_table()"))


def test_reseller_business_data(regtest, systems):
    regtest.write(f(systems, "reseller.business_data(tax_rate, depreciation_period)"))


def test_plant_net_present_value(regtest, systems):
    regtest.write(f(systems, "plant.net_present_value(*finance)"))


def test_cofiring_net_present_value(regtest, systems):
    regtest.write(f(systems, "cofiring_plant.net_present_value(*finance)"))


def test_farmer_net_present_value(regtest, systems):
    regtest.write(f(systems, "farmer.net_present_value(*finance)"))


def test_coal_saved(regtest, systems):
    set_option("display.float_format", "{:9,.1f}".format)
    regtest.write(f(systems, "coal_saved_benefits(coal_import_price)"))


def test_benefits(regtest, systems):
    regtest.write(f(systems, "benefits(discount_rate, external_cost)"))


def test_job_changes(regtest, systems):
    regtest.write(f(systems, "job_changes()"))
