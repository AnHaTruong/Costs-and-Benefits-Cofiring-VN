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
from tables import coal_saved, benefits
from tables import job_changes, energy_costs
from tables import emission_reductions

# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name

pd.options.display.float_format = '{:,.1f}'.format


@pytest.fixture()
def systems():
    return MongDuong1System, NinhBinhSystem


@pytest.fixture()
def finance():
    return discount_rate, tax_rate, depreciation_period


def test_energy_costs(regtest, systems):
    regtest.write(energy_costs(*systems))


def test_emission_reductions(regtest, systems):
    regtest.write(str(emission_reductions(*systems)))


def test_plant_lcoe_statement(regtest, systems, finance):
    series_a = systems[0].plant.lcoe_statement(*finance)
    series_b = systems[1].plant.lcoe_statement(*finance)
    regtest.write(str(series_a) + '\n' + str(series_b))


def test_cofiring_plant_lcoe_statement(regtest, systems, finance):
    series_a = systems[0].cofiring_plant.lcoe_statement(*finance)
    series_b = systems[1].cofiring_plant.lcoe_statement(*finance)
    regtest.write(str(series_a) + '\n' + str(series_b))


def test_technical_parameters(regtest, systems):
    series_a = systems[0].plant.characteristics()
    series_b = systems[1].plant.characteristics()
    regtest.write(str(series_a) + "\n" + str(series_b))


def test_income_farmer(regtest, systems):
    df_a = systems[0].farmer.income_statement()
    df_b = systems[1].farmer.income_statement()
    regtest.write(str(df_a) + "\n" + str(df_b))


def test_income_transporter(regtest, systems):
    df_a = systems[0].transporter.income_statement()
    df_b = systems[1].transporter.income_statement()
    regtest.write(str(df_a) + "\n" + str(df_b))


def test_emissions_baseline(regtest, systems):
    df_a = systems[0].emissions_baseline()
    df_b = systems[1].emissions_baseline()
    regtest.write(str(df_a) + "\n" + str(df_b))


def test_emissions_cofiring(regtest, systems):
    df_a = systems[0].emissions_cofiring()
    df_b = systems[1].emissions_cofiring()
    regtest.write(str(df_a) + "\n" + str(df_b))


def my_reg_test(regtest, systems, table):
    regtest.write(table(systems[0]) + '\n' + table(systems[1]))


def test_coal_saved(regtest, systems):
    my_reg_test(regtest, systems, coal_saved)


def test_benefits(regtest, systems):
    my_reg_test(regtest, systems, benefits)


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
