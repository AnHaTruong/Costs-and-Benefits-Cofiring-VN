# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Sandbox 2
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Timing the model run for sensitivity analysis.

Use numerical constants instead of symbolic representation of the units
decreases runtime for n=50 from 26.5 s to 2.6 s, and 2.4 s without the progress dots.
"""

import time

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

from natu import config
config.use_quantities = True

from sensitivity.blackbox import business_value as f
from sensitivity.blackbox import toy_uncertainty as problem


# Generate samples
# The number of samples generated is   saltelli_parameter * (2 num_vars + 2)

saltelli_parameter = 50

param_values = saltelli.sample(problem, saltelli_parameter)

#%% Run

t1 = time.perf_counter()

Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    print('.', end='')
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
