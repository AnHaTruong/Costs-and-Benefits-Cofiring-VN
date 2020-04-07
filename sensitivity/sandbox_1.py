# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Sandbox 1
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Sensitivity to discount rate and tax rate. Later should be 0."""

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

from sensitivity.blackbox import business_value as f
from sensitivity.blackbox import toy_uncertainty as problem

# Generate samples
# The number of samples generated is   saltelli_parameter * (2 num_vars + 2)

saltelli_parameter = 10

param_values = saltelli.sample(problem, saltelli_parameter)

#%% Run

Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    Y[i] = f(*X)

print()

#%% Perform analysis
# S1 is first order sensitivity index
# S1_conf is related to the 95% confidence intervall. Increase saltelli_parameter to narrow it.

Si = sobol.analyze(problem, Y, print_to_console=True)

# Print the first-order sensitivity indices
print(Si['S1'])
