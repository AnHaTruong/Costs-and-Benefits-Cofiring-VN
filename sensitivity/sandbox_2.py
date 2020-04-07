# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Sandbox 2
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Accelerating the model run, for sensitivity analysis.

Use numerical constants instead of symbolic representation of the units.
Decrease runtime for 50 iterations from 26.5 to 10.8 seconds.
"""

import time

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

# Here is the acceleration setting
# from natu import config
# config.use_quantities = False

from sensitivity.blackbox import business_value as f
from sensitivity.blackbox import toy_uncertainty as problem


# Generate samples
# The number of samples generated is   saltelli_parameter * (2 num_vars + 2)

saltelli_parameter = 10

param_values = saltelli.sample(problem, saltelli_parameter)

#%% Run

t1 = time.perf_counter()

Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    Y[i] = f(*X)

print()
print()
print('Time elapsed ', round(time.perf_counter() - t1, 1), 's')
print()

#%% Perform analysis
# S1 is first order sensitivity index
# S1_conf is related to the 95% confidence intervall. Increase saltelli_parameter to narrow it.

Si = sobol.analyze(problem, Y, print_to_console=True)

# Print the first-order sensitivity indices
print(Si['S1'])
