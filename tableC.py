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

from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import discount_rate, tax_rate, depreciation_period

from npv import (
            fuel_cost_coal, fuel_cost_biomass,
            operation_maintenance_cost, coal_om_cost, biomass_om_cost,
            income_tax, tot_capital_cost, discounted_total_power_gen,
            discount, cost_field_straw, cost_straw_transport
            )
from natu.math import fsum
from units import print_with_unit

print('')

row = '{:30}' + '{:8.0f}'
row1 = '{:30}' + '{:8.4f}'


def print_lcoe(plant):
    col1 = print_with_unit(tot_capital_cost(plant, 0), 'kUSD')
    col2 = print_with_unit(discount(fuel_cost_coal, plant), 'kUSD')
    col3 = print_with_unit(discount(fuel_cost_biomass, plant), 'kUSD')
    col3a = print_with_unit(discount(cost_straw_transport, plant), 'kUSD')
    col3b = print_with_unit(discount(cost_field_straw, plant), 'kUSD')
    col4 = print_with_unit(discount(operation_maintenance_cost, plant), 'kUSD')
    col4a = print_with_unit(discount(coal_om_cost, plant), 'kUSD')
    col4b = print_with_unit(discount(biomass_om_cost, plant), 'kUSD')
    col5 = print_with_unit(discount(income_tax, plant), 'kUSD')
    col6 = fsum([col1, col2, col3, col4, col5])
    col7 = discounted_total_power_gen(plant)
    col8 = col6 / col7

    col7.display_unit = 'GWh'
    col8.display_unit = 'USD/kWh'

    print(row.format('Investment', col1))
    print(row.format('Fuel cost: Coal', col2))
    print(row.format('Fuel cost: Biomass', col3))
    print(row.format('  transportation', col3a))
    print(row.format('  straw at field', col3b))
    print(row.format('O&M cost', col4))
    print(row.format('  coal', col4a))
    print(row.format('  biomass', col4b))
    print(row.format('Tax', col5))
    print(row.format('Sum of costs', col6))
    print(row.format('Electricity produced', col7))
    print(row1.format('LCOE', col8))

print('---- OLD -----')
print('Levelized cost of electricity Mong Duong 1')
print('')
print_lcoe(MongDuong1)
print('---- NEW -----')
MongDuong1Cofire.tableC(discount_rate, tax_rate, depreciation_period)

print('')
print('')
print('---- OLD -----')
print('Levelized cost of electricity Ninh Binh')
print('')
print_lcoe(NinhBinh)
print('---- NEW -----')
NinhBinhCofire.tableC(discount_rate, tax_rate, depreciation_period)
