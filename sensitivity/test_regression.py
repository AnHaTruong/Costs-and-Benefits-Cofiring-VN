# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# test_regression
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Test the code for sensitivity analysis."""

from pandas import set_option

from sensitivity.uncertainty import uncertainty_MD1, uncertainty_NB
from sensitivity.one_at_a_time import sensitivity_runs_MD1, sensitivity_runs_NB
from table_sensitivity import table_sensitivity


def test_uncertainty(regtest):
    """Save the uncertainty parameters used in sensitivity analysis."""
    set_option("display.float_format", "{:9,.2f}".format)
    regtest.write("MD1\n")
    regtest.write(uncertainty_MD1.to_string())
    regtest.write("\n\nNB\n")
    regtest.write(uncertainty_NB.to_string())


def test_results(regtest):
    set_option("display.float_format", "{:9,.2f}".format)
    regtest.write(table_sensitivity(sensitivity_runs_MD1, "Mong Duong 1"))
    regtest.write(table_sensitivity(sensitivity_runs_NB, "Ninh Binh"))
