# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# test_regression
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Test the code for sensitivity analysis."""

from sensitivity.blackbox import uncertainty
from sensitivity.one_at_a_time import sensitivity_runs_MD1, sensitivity_runs_NB


def test_uncertainty(regtest):
    regtest.write(uncertainty.to_string())


def test_results(regtest):
    regtest.write(str(sensitivity_runs_MD1))
    regtest.write(str(sensitivity_runs_NB))
