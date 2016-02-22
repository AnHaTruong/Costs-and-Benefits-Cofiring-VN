# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

from parameters import NinhBinh, MongDuong1
from parameters import time_horizon, discount_rate
from parameters import biomass_ratio, electricity_tariff_USD

print(MongDuong1.capacity)
print(NinhBinh.capacity)

print("")

from npv import npv, elec_sale_kwh, cash_inflow
from npv import tot_capital_cost, fuel_cost, net_cash_flow
from npv import operation_maintenance_cost, earning_before_tax, income_tax

print(time_horizon)
print(discount_rate)

print("")

print("Tests for NPV function")
print("")

print("Null cash flow")


def nocash(year):
    return 0
print(npv(nocash))
if npv(nocash) == 0:
    print("OK")
else:
    print("ERROR: the null cash flow should have null NPV")

print("")

print("Unit cash flow")


def unitcash(year):
    return 1
print(repr(npv(unitcash)))
CommonRatio = 1/(1+discount_rate)
SumOfGeometricSequence = (1 - CommonRatio**(time_horizon+1)) / (1 - CommonRatio)
print(repr(SumOfGeometricSequence))
if abs(npv(unitcash) - SumOfGeometricSequence) < 1E-12:
    print("OK")
else:
    print("ERROR: NPV of the unit cash flow is wrong")

print("")
print("Year")
for year in range(time_horizon+1):
    print (year,
           elec_sale_kwh(MongDuong1, year),
           round(cash_inflow(MongDuong1, year)),
           tot_capital_cost(MongDuong1, year),
           round(fuel_cost(MongDuong1, year)),
           round(earning_before_tax(MongDuong1, year)),
           round(income_tax(MongDuong1, year)),
           round(operation_maintenance_cost(MongDuong1, year)),
           round(net_cash_flow(MongDuong1, year))
           )

print("")

print ("No sales on year zero")
if elec_sale_kwh(MongDuong1, 0) == 0:
    print("OK")
else:
    print("ERROR: Electricity sales quantity Mong Duong 1 year zero ",
          elec_sale_kwh(MongDuong1, 0)
          )

print ("Sales on year one")
if elec_sale_kwh(MongDuong1, 1) == MongDuong1.generation * biomass_ratio:
    print("OK")
else:
    print("ERROR: Electricity sales quantity Mong Duong 1 year one ",
          elec_sale_kwh(MongDuong1, 1)
          )

print ("Sales remain constant")
if elec_sale_kwh(MongDuong1, 1) == elec_sale_kwh(MongDuong1, time_horizon):
    print("OK")
else:
    print("ERROR: Electricity sales quantity Mong Duong 1 different in yr 1 and yr", time_horizon)

print("")

print ("No Cash Inflow on year zero")
if cash_inflow(MongDuong1, 0) == 0:
    print("OK")
else:
    print("ERROR: Cash Inflow Mong Duong 1 year zero ",  cash_inflow(MongDuong1, 0))

print ("Cash inflow on year one")
if cash_inflow(MongDuong1, 1) == MongDuong1.generation * biomass_ratio * electricity_tariff_USD:
    print("OK")
else:
    print("ERROR: Cash Inflow Mong Duong 1 year one ",  elec_sale_kwh(MongDuong1, 1))

print ("Cash inflow remain constant")
if cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon):
    print("OK")
else:
    print("ERROR: Cash Inflow Mong Duong 1 year different in year 1 and year ", time_horizon)

print("")

print ("Total capital cost on year zero")
if tot_capital_cost(MongDuong1, 0) == MongDuong1.capital_cost * MongDuong1.capacity * biomass_ratio:
    print("OK")
else:
    print("ERROR: Total capital cost Mong Duong 1 year zero ",  tot_capital_cost(MongDuong1, 0))

print ("Capital cost on year 1 is zero")
if tot_capital_cost(MongDuong1, 1) == 0:
    print("OK")
else:
    print("ERROR: Total capital cost Mong Duong 1 year one ",  tot_capital_cost(MongDuong1, 1))

print ("Capital cost on last year is zero")
if tot_capital_cost(MongDuong1, time_horizon) == 0:
    print("OK")
else:
    print("ERROR: Total capital cost Mong Duong 1 last year ",
          tot_capital_cost(MongDuong1, time_horizon)
          )


print("")

print ("No fuel cost on year zero")
if fuel_cost(MongDuong1, 0) == 0:
    print("OK")
else:
    print("ERROR: Fuel Cost Mong Duong 1 year zero ",  fuel_cost(MongDuong1, 0))

print ("Fuel Cost on year one")
if fuel_cost(MongDuong1, 1) == MongDuong1.biomass_required * MongDuong1.biomass_unit_cost:
    print("OK")
else:
    print("ERROR: fuel_cost Mong Duong 1 year one ",  fuel_cost(MongDuong1, 1))

print ("Fuel cost remain constant")
if fuel_cost(MongDuong1, 1) == fuel_cost(MongDuong1, time_horizon):
    print("OK")
else:
    print("ERROR: Fuel Cost Mong Duong 1 year different in year 1 and year ", time_horizon)
