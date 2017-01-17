# Economic of co-firing in two power plants in Vietnam
#
#  
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print table for the net present value calculation in  npv.py
"""

from parameters import NinhBinh, MongDuong1
from parameters import time_horizon, discount_rate
# DEBUG
#time_horizon = 1

from npv import npv, cash_inflow
from npv import tot_capital_cost, fuel_cost, net_cash_flow, amortization
from npv import operation_maintenance_cost, earning_before_tax, income_tax


print('')

print('Time Horizon', time_horizon, 'years')
print('Discount Rate', discount_rate)

print('')


head = '{:4}'+' {:>11}'*9
row = '{:4d}'+' {:6.0f}'*9
print(head.format('year',
                  'elec_sale',
                  'cash_in',
                  'tot_cap',
                  'fuel_cost',
                  'amortization',
                  'EBT',
                  'income_tax',
                  'OM_cost',
                  'cash_flow')
     )


def print_npv(plant):
    """Print out the cashflows from NPV calculation in npv.py
    """

    for year in range(time_horizon+1):
        col1 = plant.elec_sale
        col2 = cash_inflow(plant, year)
        col3 = tot_capital_cost(plant, year)
        col4 = fuel_cost(plant, year)
        col5 = amortization(plant, year)
        col6 = earning_before_tax(plant, year)
        col7 = income_tax(plant, year)
        col8 = operation_maintenance_cost(plant, year)
        col9 = net_cash_flow(plant, year)

        col1.display_unit = 'GWh'
        col2.display_unit = 'kUSD'
        col3.display_unit = 'kUSD'
        col4.display_unit = 'kUSD'
        col5.display_unit = 'kUSD'
        col6.display_unit = 'kUSD'
        col7.display_unit = 'kUSD'
        col8.display_unit = 'kUSD'
        col9.display_unit = 'kUSD'

        line = row.format(year,
                          col1,
                          col2,
                          col3,
                          col4,
                          col5,
                          col6,
                          col7,
                          col8,
                          col9,
                         )
        print(line)


print('Mong Duong 1')
print_npv(MongDuong1)
print('')
print('NPV Mong Duong 1 = ', npv(MongDuong1))

print('')

print('Ninh Binh')
print_npv(NinhBinh)
print('')
print('NPV Ninh Binh  = ', npv(NinhBinh))
