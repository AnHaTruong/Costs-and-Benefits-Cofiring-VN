# Economic of co-firing in two power plants in Vietnam
#
#  NPV assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

"""Net present value assessment of a co-firing power plant
"""

from parameters import time_horizon, discount_rate, biomass_ratio
from parameters import tax_rate, depreciation_period
from units import zero_USD, zero_VND, time_step
from biomassrequired import biomass_required
from biomasscost import bm_unit_cost
from coalsaved import coal_saved


def print_with_unit(func, plant, year, unit):
    """ Display the desired unit on Tables"""
    value = func(plant, year)
    value.display_unit = unit
    return value


def cash_inflow(plant, year):
    """

    Cash inflow remain constant :
    >>> from parameters import *
    >>> cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon)
    True
    >>> cash_inflow(NinhBinh, 1) == cash_inflow(NinhBinh, time_horizon)
    True

    Cash inflow on year one:
    >>> print_with_unit(cash_inflow, MongDuong1, 1, 'kUSD')
    316073 kUSD
    >>> print_with_unit(cash_inflow, NinhBinh, 1, 'kUSD')
    41959.7 kUSD
    """
    return plant.electricity_tariff * plant.elec_sale


def cash_outflow(plant, year):
    """ This is for the whole plant

    Cash outflow year zero:
    >>> from parameters import *
    >>> print_with_unit(cash_outflow, MongDuong1, 0, 'kUSD')
    2700 kUSD
    >>> print_with_unit(cash_outflow, NinhBinh, 0, 'kUSD')
    500 kUSD

    Cash outflow from year one:
    >>> print_with_unit(cash_outflow, MongDuong1, 1, 'kUSD')
    228914 kUSD
    >>> print_with_unit(cash_outflow, NinhBinh, 1, 'kUSD')
    41024 kUSD

    """
    return (tot_capital_cost(plant, year) + fuel_cost(plant, year) +
            operation_maintenance_cost(plant, year) + income_tax(plant, year))


def tot_capital_cost(plant, year):
    """ We assume the plant is paid for coal at capacity design.
       this is only extra capital cost for the plant retrofitting for biomass co-firing  ??? Total
       This is for the whole plant

    Total capital cost is zero from year 1 afterwards:
    >>> from parameters import *
    >>> tot_capital_cost(MongDuong1, 1) == tot_capital_cost(MongDuong1, time_horizon) == zero_USD
    True
    >>> tot_capital_cost(NinhBinh, 1) == tot_capital_cost(NinhBinh, time_horizon) == zero_USD
    True

    Total capital cost on year zero:
    >>> print_with_unit(tot_capital_cost, MongDuong1, 0, 'kUSD')
    2700 kUSD
    >>> print_with_unit(tot_capital_cost, NinhBinh, 0, 'kUSD')
    500 kUSD
    """
    if year == 0:
        return plant.capital_cost * plant.capacity * biomass_ratio
    else:
        return zero_USD


def fuel_cost_coal(plant, year):
    """Fuel expense on coal

    Fuel cost on year zero
    >>> from parameters import *
    >>> print_with_unit(fuel_cost_coal, MongDuong1, 0, 'kUSD')
    137632 kUSD
    >>> print_with_unit(fuel_cost_coal, NinhBinh, 0, 'kUSD')
    35297.4 kUSD

    Fuel cost on coal from year 1
    >>> print_with_unit(fuel_cost_coal, MongDuong1, 1, 'kUSD')
    130706 kUSD
    >>> print_with_unit(fuel_cost_coal, NinhBinh, 1, 'kUSD')
    33520.5 kUSD
    """
    if year == 0:
        return plant.base_coal_consumption * plant.coal_price * time_step
    else:
        return plant.coal_price * (plant.base_coal_consumption - coal_saved(plant)) * time_step


def fuel_cost_biomass(plant, year):
    """Fuel expense on biomass

     No fuel cost on year zero
    >>> from parameters import *
    >>> print_with_unit(fuel_cost_biomass, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(fuel_cost_biomass, NinhBinh, 0, 'USD')
    0 USD

    Fuel cost on coal from year 1
    >>> print_with_unit(fuel_cost_biomass, MongDuong1, 1, 'kUSD')
    9825.15 kUSD
    >>> print_with_unit(fuel_cost_biomass, NinhBinh, 1, 'kUSD')
    1536.05 kUSD
    """
    if year == 0:
        return zero_USD
    else:
        return bm_unit_cost(plant) * biomass_required(plant) * time_step


def fuel_cost(plant, year):
    """Total expense on fuel cost including both coal and  biomass

    No fuel cost on year zero:
    >>> from parameters import *
    >>> print_with_unit(fuel_cost, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(fuel_cost, NinhBinh, 0, 'USD')
    0 USD

    Fuel cost remain constant:
    >>> fuel_cost(MongDuong1, 1) == fuel_cost(MongDuong1, time_horizon)
    True
    >>> fuel_cost(NinhBinh, 1) == fuel_cost(NinhBinh, time_horizon)
    True

    Fuel cost on year one:
    >>> print_with_unit(fuel_cost, MongDuong1, 1, 'kUSD')
    140531 kUSD
    >>> print_with_unit(fuel_cost, NinhBinh, 1, 'kUSD')
    35056.6 kUSD
    """
#    if year == 0:
#        return zero_USD
#    else:
    return fuel_cost_coal(plant, year) + fuel_cost_biomass(plant, year)
 

def operation_maintenance_cost(plant, year):
    """total expense for the plant

    No O&M cost for co-firing on the first year:
    >>> from parameters import *
    >>> print_with_unit(operation_maintenance_cost, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(operation_maintenance_cost, NinhBinh, 0, 'USD')
    0 USD

    O&M cost on year one:
    >>> print_with_unit(operation_maintenance_cost, MongDuong1, 1, 'kUSD')
    59419.6 kUSD
    >>> print_with_unit(operation_maintenance_cost, NinhBinh, 1, 'kUSD')
    5672.23 kUSD

    O&M cost remain constant from year 1 onwards:
    >>> operation_maintenance_cost(MongDuong1, 1) == operation_maintenance_cost(MongDuong1, time_horizon)
    True
    >>> operation_maintenance_cost(NinhBinh, 1) == operation_maintenance_cost(NinhBinh, time_horizon)
    True
    """
    if year == 0:
        fixed_om_coal = plant.fix_om_coal * plant.capacity * time_step
        variable_om_coal = plant.variable_om_coal * plant.elec_sale
        return fixed_om_coal + variable_om_coal
    else:
        fixed_om_bm = plant.fix_om_cost * plant.capacity * biomass_ratio * time_step
        variable_om_bm = plant.variable_om_cost * plant.elec_sale * biomass_ratio
        fixed_om_coal = plant.fix_om_coal * plant.capacity * (1 - biomass_ratio) * time_step
        variable_om_coal = plant.variable_om_coal * plant.elec_sale * (1 - biomass_ratio)
        return fixed_om_bm + variable_om_bm + fixed_om_coal + variable_om_coal


def income_tax(plant, year):
    """Corporate tax
    No income tax for co-firing on the first year:
    >>> from parameters import *
    >>> print_with_unit(income_tax, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(income_tax, NinhBinh, 0, 'USD')
    0 USD

    Income tax on year 1:
    >>> print_with_unit(income_tax, MongDuong1, 1, 'kUSD')
    28963 kUSD
    >>> print_with_unit(income_tax, NinhBinh, 1, 'kUSD')
    295.208 kUSD

    """
#    if year == 0:
#        return zero_VND
#    else:
    if earning_before_tax(plant, year) > zero_VND:
        return tax_rate * earning_before_tax(plant, year)
    else:
        return zero_VND


def amortization(plant, year):
    """Amortization of the investment cost

    No amortization on year 0
    >>> from parameters import *
    >>> print_with_unit(amortization, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(amortization, NinhBinh, 0, 'USD')
    0 USD

    Amortization on year 1:
    >>> print_with_unit(amortization, MongDuong1, 1, 'kUSD')
    270 kUSD
    >>> print_with_unit(amortization, NinhBinh, 1, 'kUSD')
    50 kUSD

   """
    if year == 0:
        return zero_VND
    else:

        if year in range(1, depreciation_period + 1):
            return tot_capital_cost(plant, 0) / float(depreciation_period)
        else:
            return zero_VND


def earning_before_tax(plant, year):
    """
    No earning before tax for co-firing on the first year:
    >>> from parameters import *
    >>> print_with_unit(earning_before_tax, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(earning_before_tax, NinhBinh, 0, 'USD')
    0 USD

    Earning before tax on year 1:
    >>> print_with_unit(earning_before_tax, MongDuong1, 1, 'kUSD')
    115852 kUSD
    >>> print_with_unit(earning_before_tax, NinhBinh, 1, 'kUSD')
    1180.83 kUSD
    """
#    if year == 0:
#      return zero_VND
#    else:  
    return (cash_inflow(plant, year) -
            fuel_cost(plant, year) -
            operation_maintenance_cost(plant, year) -
            amortization(plant, year)
            )


def net_cash_flow(plant, year):
    """Cash flow of the plant

    Net cash flow on year 0:
    >>> from parameters import *
    >>> print_with_unit(net_cash_flow, MongDuong1, 0, 'kUSD')
    -2700 kUSD
    >>> print_with_unit(net_cash_flow, NinhBinh, 0, 'kUSD')
    -500 kUSD

    Net cash flow on year 1:
    >>> print_with_unit(net_cash_flow, MongDuong1, 1, 'kUSD')
    87158.9 kUSD
    >>> print_with_unit(net_cash_flow, NinhBinh, 1, 'kUSD')
    935.624 kUSD
    """
    return cash_inflow(plant, year) - cash_outflow(plant, year)


def npv(plant):
    """npv returns the Net Present Value of the project,
    discounted at DiscountRate from 0 to TimeHorizon included
    >>> from parameters import *
    >>> npv(MongDuong1)
    8.05546e+08 USD
    >>> npv(NinhBinh)
    8.14337e+06 USD
    """
    value = zero_USD
    for year in range(time_horizon+1):
        value += net_cash_flow(plant, year) / (1+discount_rate)**year
    return value

if __name__ == "__main__":
    import doctest
    doctest.testmod()
