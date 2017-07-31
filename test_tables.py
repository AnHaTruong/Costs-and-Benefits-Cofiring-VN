# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Test the boundary case: cofiring biomass ratio 0% is same as baseline plant."""

import pytest

import parameters as baseline

from table_technical_parameters import technical_parameters
from table_coal_saved import coal_saved
from table_benefits import benefits
from table_emissions import emissions
from table_upstream_benefits import upstream_benefits
from table_job_changes import job_changes
from table_energy_costs import energy_costs
from table_lcoe import lcoe

# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name


@pytest.fixture()
def systems():
    return baseline.MongDuong1System, baseline.NinhBinhSystem


def test_energy_costs(regtest, systems):
    regtest.write(energy_costs(*systems))


def test_technical_parameters(regtest, systems):
    regtest.write(technical_parameters(*systems))


def my_reg_test(regtest, systems, table):
    regtest.write(table(systems[0]) + '\n' + table(systems[1]))


def test_coal_saved(regtest, systems):
    my_reg_test(regtest, systems, coal_saved)


def test_benefits(regtest, systems):
    my_reg_test(regtest, systems, benefits)


def test_emissions(regtest, systems):
    my_reg_test(regtest, systems, emissions)


def test_lcoe(regtest, systems):
    my_reg_test(regtest, systems, lcoe)


def test_upstream_benefits(regtest, systems):
    my_reg_test(regtest, systems, upstream_benefits)


def test_job_changes(regtest, systems):
    my_reg_test(regtest, systems, job_changes)


def test_net_present_value_plant(regtest, systems):
    table_a = systems[0].plant.pretty_table(
        baseline.discount_rate,
        baseline.tax_rate,
        baseline.depreciation_period)
    table_b = systems[1].plant.pretty_table(
        baseline.discount_rate,
        baseline.tax_rate,
        baseline.depreciation_period)
    regtest.write(table_a + '\n' + table_b)


def test_net_present_value_cofiring(regtest, systems):
    table_a = systems[0].cofiring_plant.pretty_table(
        baseline.discount_rate,
        baseline.tax_rate,
        baseline.depreciation_period)
    table_b = systems[1].cofiring_plant.pretty_table(
        baseline.discount_rate,
        baseline.tax_rate,
        baseline.depreciation_period)
    regtest.write(table_a + '\n' + table_b)
