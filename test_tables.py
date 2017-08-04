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
from tables import technical_parameters, coal_saved, benefits, emissions, upstream_benefits
from tables import job_changes, energy_costs, lcoe
from tables import emission_reductions, balance_sheet_farmer, balance_sheet_transporter

# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name

pd.options.display.float_format = '{:,.1f}'.format


@pytest.fixture()
def systems():
    return MongDuong1System, NinhBinhSystem


def test_energy_costs(regtest, systems):
    regtest.write(energy_costs(*systems))


def test_technical_parameters(regtest, systems):
    regtest.write(technical_parameters(*systems))


def test_emission_reductions(regtest, systems):
    regtest.write(str(emission_reductions(*systems)))


def test_balance_sheet_farmer(regtest, systems):
    regtest.write(str(balance_sheet_farmer(*systems)))


def test_balance_sheet_transporter(regtest, systems):
    regtest.write(str(balance_sheet_transporter(*systems)))


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
    table_a = systems[0].plant.pretty_table(discount_rate, tax_rate, depreciation_period)
    table_b = systems[1].plant.pretty_table(discount_rate, tax_rate, depreciation_period)
    regtest.write(table_a + '\n' + table_b)


def test_net_present_value_cofiring(regtest, systems):
    table_a = systems[0].cofiring_plant.pretty_table(discount_rate, tax_rate, depreciation_period)
    table_b = systems[1].cofiring_plant.pretty_table(discount_rate, tax_rate, depreciation_period)
    regtest.write(table_a + '\n' + table_b)
