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
from parameters import MongDuong1

# Only run interactively, for now
try:
    __IPYTHON__
except NameError:
    exit()   # Quietly


# The depreciation period is an discrete parameter. See item 2 on the list at
# https://waterprogramming.wordpress.com/2014/02/11/
# extensions-of-salib-for-more-complex-sensitivity-analyses/
# TLDR: Warning the Morris method is affected

problem = {'num_vars': 3,
           'names': ['discount_rate', 'tax_rate', 'depreciation_period'],
           'bounds': [[0, 0.15],
                      [0, 0.25],
                      [1, TIMEHORIZON - 1]]
           }

param_values = saltelli.sample(problem, 100, calc_second_order=True)

Y = np.empty([param_values.shape[0]])


def model(args):
    """Sandbox to test the API."""
    return MongDuong1.net_present_value(args[0], args[1], int(args[2])) / USD


for i, X in enumerate(param_values):
    Y[i] = model(X)

Si = sobol.analyze(problem, Y, print_to_console=False)

print(Si['S1'])
print(Si['S1_conf'])

print(Si['ST'])

print("x1-x2:", Si['S2'][0, 1])
print("x1-x3:", Si['S2'][0, 2])
print("x2-x3:", Si['S2'][1, 2])
