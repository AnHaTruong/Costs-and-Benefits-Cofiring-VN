# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# blackbox
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Represents the model as a blackbox, for sensitivity analysis.

Sensitivity analysis is based on the representation  Y = f(X1, ..., Xn).
"""

from model.utils import USD

from manuscript1.parameters import MongDuong1System

toy_uncertainty = {
    'num_vars': 2,
    'names': ['discount_rate', 'tax_rate'],
    'bounds': [[0.03, 0.15],    # Discount rate
               [0, 0.4]]        # Tax rate
}


# We know the tax rate does not matter, but we want to check that the sensitivity computes to 0
# pylint: disable=unused-argument
def business_value(discount_rate, tax_rate):
    """Return for Y the business value of cofiring."""
    result = MongDuong1System.table_business_value(discount_rate)[-1] / USD
    return result
