# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Sandbox 2
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Discovering SALib for sensitivity analysis.

Use numerical constants instead of symbolic representation of the units
decreases runtime for n=50 from 26.5 s to 2.6 s, and 2.4 s without the progress dots.
"""

import os
import time
import cProfile

import numpy as np

from SALib.sample import saltelli
from SALib.analyze import sobol

from natu import config
config.use_quantities = False

from sensitivity.blackbox import toy_business_value as f
from sensitivity.blackbox import toy_uncertainty as problem


# Generate samples
# The number of samples generated is   saltelli_parameter * (2 num_vars + 2)

saltelli_parameter = 50

param_values = saltelli.sample(problem, saltelli_parameter)

#%% Basic run

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


#%% Timed run

t1 = time.perf_counter()

Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    # print('.', end='')
    Y[i] = f(*X)

print()
print()
print('Time elapsed ', round(time.perf_counter() - t1, 1), 's')
print()

#%% Run faster, and comprehension looks less pedestrian than the loop

t1 = time.perf_counter()

Y_list = [f(*x) for x in param_values]

Y = np.array(Y_list)

print()
print()
print('Time elapsed ', round(time.perf_counter() - t1, 1), 's')
print()

#%% Run even faster.
# Optimizing the main outer loop does not brings much, but looks hard to read.

t1 = time.perf_counter()

Y_iterable = (f(*x) for x in param_values)

Y = np.fromiter(Y_iterable, float, count=len(param_values))

print()
print()
print('Time elapsed ', round(time.perf_counter() - t1, 1), 's')
print()


#%% Profiling: wrap the run in a function

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


cProfile.run("do_runs(param_values)", 'run_profile')

# Assuming  snakeviz  is installed
os.system('snakeviz run_profile')