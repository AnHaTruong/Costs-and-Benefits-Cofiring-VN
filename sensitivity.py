# Economic of co-firing in two power plants in Vietnam
#
# Sensitivity analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

import timeit

from SALib.sample import saltelli
from SALib.analyze import sobol

from natu import config
config.use_quantities = False

from init import time_horizon, USD, np
from parameters import MongDuong1
# from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire


# The depreciation period is an discrete parameter.
#  -> Warning the Morris method is affected
# https://waterprogramming.wordpress.com/2014/02/11/extensions-of-salib-for-more-complex-sensitivity-analyses/ (item 2 on the list)

problem = {'num_vars': 3,
           'names': ['discount_rate', 'tax_rate', 'depreciation_period'],
           'bounds': [[0, 0.15],
                      [0, 0.25],
                      [1, time_horizon - 1]]
           }

param_values = saltelli.sample(problem, 100, calc_second_order=True)

Y = np.empty([param_values.shape[0]])


def model(X):
    return (MongDuong1.net_present_value(X[0], X[1], int(X[2])) / USD)

for i, X in enumerate(param_values):
    Y[i] = model(X)


def test():
    """Stupid test function"""
    Si = sobol.analyze(problem, Y, print_to_console=False)
    return Si

print(timeit.timeit('test()', setup='from __main__ import test', number=3))

#print(Si['S1'])
#print(Si['S1_conf'])
#
#print(Si['ST'])
#
#print("x1-x2:", Si['S2'][0, 1])
#print("x1-x3:", Si['S2'][0, 2])
#print("x2-x3:", Si['S2'][1, 2])
