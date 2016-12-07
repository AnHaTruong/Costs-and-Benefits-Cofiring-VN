# Simplified NPV model for SALib test
"""
Created on Tue Aug 30 15:39:06 2016

@author: anha
"""

from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

#NPV model
electricity_tariff = 1500
time_horizon = 20
elec_sale = 6500000000000
biomass_required = 259107

def npv(electricity_tariff, bm_unit_cost, discount_rate):
    """npv returns the Net Present Value of the project,
    discounted at DiscountRate from 0 to TimeHorizon included
    """
    value = 0
    for year in range(time_horizon+1):
        value += net_cash_flow(electricity_tariff, bm_unit_cost) / (1+discount_rate)**year
    return value
    
    
def net_cash_flow(electricity_tariff, bm_unit_cost):
     return cash_inflow(electricity_tariff) - cash_outflow(bm_unit_cost)
     
     
def cash_inflow(electricity_tariff):
    return electricity_tariff * elec_sale
    
    
def cash_outflow(bm_unit_cost):
    return fuel_cost(bm_unit_cost)
    

def fuel_cost(bm_unit_cost):
    return bm_unit_cost * biomass_required




# Define the model inputs
problem = { 
            'num_vars': 3,
            'name': ['electricity_tariff','biomass_unit_cost', 'discount_rate'], 
            'bounds': [[1000, 2000],
                       [20, 60],
                       [0.0, 0.1]                    
                      ]
          }


# Generate samples

param_values = saltelli.sample(problem, 1000, calc_second_order = True)

#print(param_values)
    
# Run model
Y = np.empty([param_values.shape[0]])
for i, X in enumerate(param_values):
    Y[i] = npv(*X)

# Perform analysis
Si = sobol.analyze(problem, Y, print_to_console = False)

# Print the first order sensitivity indices

print(Si['S1'])
print(Si['S1_conf'])

# Print the second order sensitivity indices

print(Si['ST'])
print(Si['ST_conf'])

