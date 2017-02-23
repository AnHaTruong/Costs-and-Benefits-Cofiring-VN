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

from parameters import MongDuong1, NinhBinh, discount_rate, depreciation_period
from units import time_horizon
# DEBUG
#time_horizon = 1

from npv import (
            net_present_value, cash_inflow, sales,
            tot_capital_cost, fuel_cost, net_cash_flow, amortization,
            operation_maintenance_cost, earning_before_tax, income_tax
            )


print('')

print('Time Horizon', time_horizon, 'years')
print('Discount Rate', discount_rate)
print('Depreciation', depreciation_period, 'years')

print('')


def print_tableA(plant):
    """Print out the cashflows from NPV calculation in npv.py
    """
    print(plant.name)
    result = net_present_value(plant)
    result.display_unit = 'kUSD'
    print('NPV = ', result)

    head = '{:4}{:>12}{:>12}{:>12}{:>12}{:>12}{:>12}{:>12}{:>12}{:>12}'
    row = '{:4d}'+' {:6.0f}'*9

    print(head.format('year',
                      'cash_in',
                      'tot_cap',
                      'amortizatin',
                      'fuel_cost',
                      'EBT',
                      'income_tax',
                      'OM_cost',
                      'cash_flow',
                      'elec_sale'
                      )
          )

    for year in range(time_horizon+1):
        col1 = sales(plant, year)
        col2 = cash_inflow(plant, year)
        col3 = tot_capital_cost(plant, year)
        col4 = amortization(plant, year)
        col5 = fuel_cost(plant, year)
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
                          col2,
                          col3,
                          col4,
                          col5,
                          col6,
                          col7,
                          col8,
                          col9,
                          col1
                          )
        print(line)


print_tableA(MongDuong1)

print('')

print_tableA(NinhBinh)
