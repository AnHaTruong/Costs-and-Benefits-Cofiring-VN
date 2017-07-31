# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Sensitivity analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""WORK IN PROGRESS."""

import numpy as np

from SALib.sample import saltelli
from SALib.analyze import sobol

#from natu import config
# module configuration must be done BEFORE using it in the imported module
#pylint: disable=wrong-import-position
#config.use_quantities = False

from init import TIMEHORIZON, USD
import parameters as baseline


# The depreciation period is an discrete parameter. See item 2 on the list at
# https://waterprogramming.wordpress.com/2014/02/11/
# extensions-of-salib-for-more-complex-sensitivity-analyses/
# TLDR: Warning the Morris method is affected


def model(args):
    """Sandbox to test the API."""
    return baseline.MongDuong1System.plant.net_present_value(args[0], args[1], int(args[2])) / USD


def sensitivy_analysis():
    """Compute first and second order sensitivity of cofiring project's net present value.

    Variables: discount rate, tax rate, depreciation period
    """
    problem = {'num_vars': 3,
               'names': ['discount_rate', 'tax_rate', 'depreciation_period'],
               'bounds': [[0, 0.15],
                          [0, 0.25],
                          [1, TIMEHORIZON - 1]]}

    param_values = saltelli.sample(problem, 100, calc_second_order=True)

    results = np.empty([param_values.shape[0]])
    for i, parameter in enumerate(param_values):
        results[i] = model(parameter)

    sensitivity_indices = sobol.analyze(problem, results, print_to_console=False)

    print(sensitivity_indices['S1'])
    print(sensitivity_indices['S1_conf'])

    print(sensitivity_indices['ST'])

    print("x1-x2:", sensitivity_indices['S2'][0, 1])
    print("x1-x3:", sensitivity_indices['S2'][0, 2])
    print("x2-x3:", sensitivity_indices['S2'][1, 2])

# Do nothing for now...
