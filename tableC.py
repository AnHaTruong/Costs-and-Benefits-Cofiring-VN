# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity(LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""print the LCOE calculation results in file lcoe.py"""

from parameters import MongDuong1, NinhBinh
from parameters import time_horizon, discount_rate

#from lcoe import lcoe_investment, lcoe_fuel_coal, lcoe_fuel_biomass
#from lcoe import lcoe_om, lcoe_tax, lcoe_cost, lcoe_power_gen, lcoe
from lcoe import discount, lcoe_power_gen
from npv import fuel_cost_coal, fuel_cost_biomass, operation_maintenance_cost
from npv import income_tax, tot_capital_cost
from natu.math import fsum
from units import print_with_unit

print('')

print('')

row = '{:30}' + '{:8.0f}'
row1 = '{:30}' + '{:8.4f}'


def print_lcoe(plant):
    
    col1 = print_with_unit(tot_capital_cost(plant, 0), 'kUSD')
    col2 = print_with_unit(discount(fuel_cost_coal, plant, time_horizon, discount_rate), 'kUSD')
    col3 = print_with_unit(discount(fuel_cost_biomass, plant, time_horizon, discount_rate), 'kUSD')
    col4 = print_with_unit(discount(operation_maintenance_cost, plant, time_horizon, discount_rate), 'kUSD')
    col5 = print_with_unit(discount(income_tax, plant, time_horizon, discount_rate), 'kUSD')
    col6 = fsum([col2, col3, col4, col5])
    col7 = lcoe_power_gen(plant)
    col8 = col6 / col7
    
    col7.display_unit = 'GWh'
    col8.display_unit = 'USD/kWh'
       
    print(row.format('Investment', col1))
    print(row.format('Fuel cost: Coal', col2))
    print(row.format('Fuel cost: Biomass', col3))
    print(row.format('O&M cost', col4))
    print(row.format('Tax', col5))
    print(row.format('Sum of costs', col6))
    print(row.format('Electricity produced', col7))
    print(row1.format('LCOE', col8))
    
    
print('Levelized cost of electricity Mong Duong 1')
print('')
print_lcoe(MongDuong1)

print('')
print('')
print('Levelized cost of electricity Ninh Binh')
print('')

print_lcoe(NinhBinh)

