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

from classdef import MongDuong1, NinhBinh

from lcoe import lcoe_investment, lcoe_fuel_coal, lcoe_fuel_biomass
from lcoe import lcoe_om, lcoe_tax, lcoe_cost, lcoe_power_gen, lcoe


print('')

print('')

row = '{:30}' + '{:8.0f}'
row1 = '{:30}' + '{:8.4f}'

#print (head.format(' ', 'Mong Duong 1', 'Ninh Binh'))


def print_lcoe(plant):
    
    col1 = lcoe_investment(plant)
    col2 = lcoe_fuel_coal(plant)
    col3 = lcoe_fuel_biomass(plant)
    col4 = lcoe_om(plant)
    col5 = lcoe_tax(plant)
    col6 = lcoe_cost(plant)
    col7 = lcoe_power_gen(plant)
    col8 = lcoe(plant)
    
    col1.display_unit = 'kUSD'
    col2.display_unit = 'kUSD'
    col3.display_unit = 'kUSD'
    col4.display_unit = 'kUSD'
    col5.display_unit = 'kUSD'
    col6.display_unit = 'kUSD'
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
