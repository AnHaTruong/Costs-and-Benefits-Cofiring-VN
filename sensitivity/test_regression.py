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

# pylint: disable=wrong-import-position
from natu import config

config.use_quantities = False

from sensitivity.uncertainty import uncertainty_MD1, uncertainty_NB
from sensitivity.one_at_a_time import table_sensitivity
from sensitivity.blackbox import f_MD1, f_NB


def test_uncertainty(regtest):
    """Save the uncertainty parameters used in sensitivity analysis."""
    set_option("display.float_format", "{:9,.2f}".format)
    regtest.write("MD1\n")
    regtest.write(uncertainty_MD1.to_string())
    regtest.write("\n\nNB\n")
    regtest.write(uncertainty_NB.to_string())


def test_results(regtest):
    set_option("display.float_format", "{:9,.2f}".format)
    regtest.write(table_sensitivity(uncertainty_MD1, f_MD1, "Mong Duong 1"))
    regtest.write(table_sensitivity(uncertainty_NB, f_NB, "Ninh Binh"))
