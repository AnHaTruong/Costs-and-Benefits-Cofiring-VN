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
from parameters import time_step, time_horizon, discount_rate
from parameters import biomass_ratio, electricity_tariff
from parameters import zero_kwh, zero_VND

from npv import npv, elec_sale, cash_inflow
from npv import tot_capital_cost, fuel_cost, net_cash_flow
from npv import operation_maintenance_cost, earning_before_tax, income_tax


print(MongDuong1.capacity)
print(NinhBinh.capacity)

print('')

print(time_horizon)
print(discount_rate)

print('')
head = '{:4}'+' {:>10}'*8
row = '{:4d}'+' {:10.0f}'*8
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

print('Cash inflow on year one')
if cash_inflow(MongDuong1, 1) == MongDuong1.generation * biomass_ratio * electricity_tariff * time_step:
    print('OK')
else:
    print('ERROR: Cash Inflow Mong Duong 1 year one ', elec_sale(MongDuong1, 1))

print('Cash inflow remain constant')
if cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon):
    print('OK')
else:
    print('ERROR: Cash Inflow Mong Duong 1 year different in year 1 and year ', time_horizon)

print('')

print('Total capital cost on year zero')
if tot_capital_cost(MongDuong1, 0) == MongDuong1.capital_cost * MongDuong1.capacity * biomass_ratio:
    print('OK')
else:
    print('ERROR: Total capital cost Mong Duong 1 year zero ', tot_capital_cost(MongDuong1, 0))

print('')

print('Fuel Cost on year one')
if fuel_cost(MongDuong1, 1) == MongDuong1.biomass_required * MongDuong1.biomass_unit_cost * time_step:
    print('OK')
else:
    print('ERROR: fuel_cost Mong Duong 1 year one ', fuel_cost(MongDuong1, 1))
    print(MongDuong1.biomass_required * MongDuong1.biomass_unit_cost)


print()
print('NPV = {:10.0f}'.format(npv(MongDuong1)))
print('NPV = {:10.0f}'.format(npv(NinhBinh)))
