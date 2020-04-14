# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# test_regression
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Test the code for sensitivity analysis."""

from sensitivity.one_at_a_time import df


def test_parameters(regtest):
    regtest.write(df.to_string())
