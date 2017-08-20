# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Test the boundary case: cofiring biomass ratio 0% is same as baseline plant."""

import pytest
import pandas as pd

from parameters import MongDuong1System, NinhBinhSystem
from parameters import discount_rate, tax_rate, depreciation_period
# We are using them inside an eval string
# pylint: disable=unused-import
from parameters import external_cost, coal_import_price, mining_parameter
from tables import energy_costs, straw_supply, emission_reductions

# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name

pd.options.display.float_format = '{:,.1f}'.format

finance = discount_rate, tax_rate, depreciation_period


@pytest.fixture()
def systems():
    return MongDuong1System, NinhBinhSystem


def test_energy_costs(regtest, systems):
    regtest.write(energy_costs(*systems))


def test_emission_reductions(regtest, systems):
    regtest.write(str(emission_reductions(*systems)))


def test_straw_supply(regtest, systems):
    regtest.write(straw_supply(*systems))


# pylint: disable=eval-used, unused-argument
def f(systems, method):
    result_a = eval('systems[0].' + method)
    result_b = eval('systems[1].' + method)
    return str(result_a) + "\n\n" + str(result_b)


def test_plant_lcoe_statement(regtest, systems):
    regtest.write(f(systems, 'plant.lcoe_statement(*finance)'))


def test_cofiring_plant_lcoe(regtest, systems):
    regtest.write(f(systems, 'cofiring_plant.lcoe_statement(*finance)'))


def test_technical_parameters(regtest, systems):
    regtest.write(f(systems, 'plant.characteristics()'))


def test_income_farmer(regtest, systems):
    regtest.write(f(systems, 'farmer.earning_before_tax_detail()'))


def test_income_transporter(regtest, systems):
    regtest.write(f(systems, 'transporter.earning_before_tax_detail()'))


def test_emissions_baseline(regtest, systems):
    regtest.write(f(systems, 'emissions_baseline()'))


def test_emissions_cofiring(regtest, systems):
    regtest.write(f(systems, 'emissions_cofiring()'))


def test_net_present_value_plant(regtest, systems):
    regtest.write(f(systems, 'plant.pretty_table(*finance)'))


def test_net_present_value_cofiring(regtest, systems):
    regtest.write(
        f(systems, 'cofiring_plant.pretty_table(*finance)'))


def test_farmer_pretty_table(regtest, systems):
    regtest.write(
        f(systems, 'farmer.pretty_table(*finance)'))


def test_coal_saved(regtest, systems):
    regtest.write(f(systems, 'coal_saved_benefits(coal_import_price)'))


def test_benefits(regtest, systems):
    regtest.write(f(systems, 'benefits(discount_rate, external_cost)'))


def test_job_changes(regtest, systems):
    regtest.write(f(systems, 'job_changes(mining_parameter)'))
