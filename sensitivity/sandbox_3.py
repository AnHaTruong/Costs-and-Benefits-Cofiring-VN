# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Sandbox 3
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Profiling the model runs, for sensitivity analysis.

Build upon sandbox 2: Use numerical constants instead of symbolic representation of the units.
"""

import time

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

# import cProfile

# from natu import config
# config.use_quantities = False

from sensitivity.blackbox import business_value as f
from sensitivity.blackbox import toy_uncertainty as problem

# Generate samples
# The number of samples generated is   saltelli_parameter * (2 num_vars + 2)

saltelli_parameter = 5

param_values = saltelli.sample(problem, saltelli_parameter)

#%% Run

Y = np.zeros([param_values.shape[0]])


def do_runs(parameter_values):
    """Perform the Monte Carlo analysis."""
    t1 = time.perf_counter()
    for i, X in enumerate(parameter_values):
        Y[i] = f(*X)
        print('.', end='')
    print()
    runtime = round(time.perf_counter() - t1, 1)
    print()
    print('Time elapsed ', runtime, 's')
    print()
    return runtime


do_runs(param_values)

# cProfile.run("do_runs(param_values)", 'run_profile')

#%% Perform analysis
# S1 is first order sensitivity index
# S1_conf is related to the 95% confidence intervall. Increase saltelli_parameter to narrow it.

Si = sobol.analyze(problem, Y, print_to_console=True)

# Print the first-order sensitivity indices
print()
print(Si['S1'])
