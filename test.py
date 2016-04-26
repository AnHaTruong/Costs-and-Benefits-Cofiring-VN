# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Tests for the net present value functions in  npv.py
"""

from parameters import NinhBinh, MongDuong1
from parameters import time_horizon, discount_rate

from npv import npv, elec_sale, cash_inflow
from npv import tot_capital_cost, fuel_cost, net_cash_flow
from npv import operation_maintenance_cost, earning_before_tax, income_tax


print(MongDuong1.capacity)
print(NinhBinh.capacity)

print('')

print(time_horizon)
print(discount_rate)

print('')
print('Mong Duong 1')

head = '{:4}'+' {:>11}'*8
row = '{:4d}'+' {:~P 10.0f}'*8
print(head.format('year',
                  'elec_sale',
                  'cash_in',
                  'tot_cap',
                  'fuel_cost',
                  'EBT',
                  'income_tax',
                  'OM_cost',
                  'cash_flow')
      )

for year in range(time_horizon+1):
    line = row.format(year,
                      elec_sale(MongDuong1, year),
                      cash_inflow(MongDuong1, year),
                      tot_capital_cost(MongDuong1, year),
                      fuel_cost(MongDuong1, year),
                      earning_before_tax(MongDuong1, year),
                      income_tax(MongDuong1, year),
                      operation_maintenance_cost(MongDuong1, year),
                      net_cash_flow(MongDuong1, year)
                      )
    print(line)

print('')
print('Ninh Binh')

for year in range(time_horizon+1):
    line = row.format(year,
                      elec_sale(NinhBinh, year),
                      cash_inflow(NinhBinh, year),
                      tot_capital_cost(NinhBinh, year),
                      fuel_cost(NinhBinh, year),
                      earning_before_tax(NinhBinh, year),
                      income_tax(NinhBinh, year),
                      operation_maintenance_cost(NinhBinh, year),
                      net_cash_flow(NinhBinh, year)
                      )
    print(line)

print('')

print()
print('NPV = {:10.0f}'.format(npv(MongDuong1)))
print('NPV = {:10.0f}'.format(npv(NinhBinh)))
