from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

from model.utils import USD

from manuscript1.parameters import MongDuong1System  #, NinhBinhSystem

# Sandbox 1. :  Sensitivity to discount rate and tax rate. Later should be 0.

# Define the model inputs
problem = {
    'num_vars': 2,
    'names': ['discount_rate', 'tax_rate'],
    'bounds': [[0.03, 0.15],    # Discount rate
               [0, 0.4]]        # Tax rate
}

# Generate samples
# The number of samples generated is   saltelli_parameter * (2 num_vars + 2)
  
saltelli_parameter = 10

param_values = saltelli.sample(problem, saltelli_parameter)

#%% Run

def business_value(discount_rate, tax_rate):
    result = MongDuong1System.table_business_value(discount_rate)[-1] / USD
    print('.', end='')
    return result

Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    Y[i] = business_value(*X)

print()

#%% Perform analysis
# S1 is first order sensitivity index
# S1_conf is related to the 95% confidence intervall. Increase saltelli_parameter to narrow it.

Si = sobol.analyze(problem, Y, print_to_console=True)

# Print the first-order sensitivity indices
print(Si['S1'])