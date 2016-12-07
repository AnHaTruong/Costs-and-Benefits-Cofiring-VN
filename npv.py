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

from parameters import time_step, time_horizon, discount_rate, biomass_ratio
from parameters import tax_rate, depreciation_period
from parameters import zero_kwh, zero_USD, zero_VND
from biomassrequired import biomass_required
from biomasscost import bm_unit_cost
from coalsaved import coal_saved, base_coal_consumption


def print_with_unit(func, plant, year, unit):
    """ Display the desired unit on Tables"""
    value = func(plant, year)
    value.display_unit = unit
    return value


def power_generation(plant):
    return plant.capacity * plant.capacity_factor


def elec_sale(plant, year):
    """
        this is for the whole plant

     In the first year, the project is not here yet so no sales:
     >>> from parameters import *
     >>> elec_sale(MongDuong1, 0)
     0 hr*kW
     >>> elec_sale(NinhBinh, 0)
     0 hr*kW

     From the second year onwards:
     >>> print_with_unit(elec_sale, MongDuong1, 1, 'GWh')
     4733.64 GWh
     >>> print_with_unit(elec_sale, NinhBinh, 1, 'GWh')
     561.024 GWh

     Sales are assumed constant afterwards:
     >>> elec_sale(MongDuong1, 1) == elec_sale(MongDuong1, time_horizon)
     True
     >>> elec_sale(NinhBinh, 1) == elec_sale(NinhBinh, time_horizon)
     True
    """
    if year == 0:
        return zero_kwh
    else:
        return power_generation(plant) * time_step


def cash_inflow(plant, year):
    """ Excel line 99 and 102
        This is for the whole plant

    In the first year, there is no sale so cash inflow is zero:
    >>> from parameters import *
    >>> print_with_unit(cash_inflow, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(cash_inflow, NinhBinh, 0, 'USD')
    0 USD

    Cash inflow remain constant afterwards:
    >>> cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon)
    True
    >>> cash_inflow(NinhBinh, 1) == cash_inflow(NinhBinh, time_horizon)
    True

    Cash inflow on year one:
    >>> print_with_unit(cash_inflow, MongDuong1, 1, 'kUSD')
    361680 kUSD
    >>> print_with_unit(cash_inflow, NinhBinh, 1, 'kUSD')
    56093.4 kUSD
    """
    return plant.electricity_tariff * elec_sale(plant, year)


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
    245280 kUSD
    >>> print_with_unit(cash_outflow, NinhBinh, 1, 'kUSD')
    44544.2 kUSD

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
    
    No fuel cost on year zero    
    >>> from parameters import *
    >>> print_with_unit(fuel_cost_coal, MongDuong1, 0, 'USD')
    0 USD
    >>> print_with_unit(fuel_cost_coal, NinhBinh, 0, 'USD')
    0 USD
    
    Fuel cost on coal from year 1    
    >>> print_with_unit(fuel_cost_coal, MongDuong1, 1, 'kUSD')
    131867 kUSD
    >>> print_with_unit(fuel_cost_coal, NinhBinh, 1, 'kUSD')
    32056.9 kUSD
    """
    if year == 0:
        return zero_USD
    else:
        return plant.coal_price * (base_coal_consumption(plant) - coal_saved(plant)) * time_step
        
        
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
    11300.5 kUSD
    >>> print_with_unit(fuel_cost_biomass, NinhBinh, 1, 'kUSD')
    2063.64 kUSD
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
    143167 kUSD
    >>> print_with_unit(fuel_cost, NinhBinh, 1, 'kUSD')
    34120.5 kUSD
    """
    if year == 0:
        return zero_USD
    else:
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
    63403 kUSD
    >>> print_with_unit(operation_maintenance_cost, NinhBinh, 1, 'kUSD')
    6590.65 kUSD

    O&M cost remain constant from year 1 onwards:
    >>> operation_maintenance_cost(MongDuong1, 1) == operation_maintenance_cost(MongDuong1, time_horizon)
    True
    >>> operation_maintenance_cost(NinhBinh, 1) == operation_maintenance_cost(NinhBinh, time_horizon)
    True
    """
    if year == 0:
        return zero_USD
    else:
        fixed_om_bm = plant.fix_om_cost * plant.capacity * biomass_ratio * time_step
        variable_om_bm = plant.variable_om_cost * elec_sale(plant, year) * biomass_ratio
        fixed_om_coal = plant.fix_om_coal * plant.capacity * (1 - biomass_ratio) * time_step
        variable_om_coal = plant.variable_om_coal * elec_sale(plant, year) * (1 - biomass_ratio)
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
    38709.8 kUSD
    >>> print_with_unit(income_tax, NinhBinh, 1, 'kUSD')
    3833.06 kUSD

    """
    if year == 0:
        return zero_VND
    else:
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
    154839 kUSD
    >>> print_with_unit(earning_before_tax, NinhBinh, 1, 'kUSD')
    15332.2 kUSD
    """
    if year == 0:
        return zero_VND
    else:
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
    116399 kUSD
    >>> print_with_unit(net_cash_flow, NinhBinh, 1, 'kUSD')
    11549.2 kUSD

    """
    return cash_inflow(plant, year) - cash_outflow(plant, year)


def npv(plant):
    """npv returns the Net Present Value of the project,
    discounted at DiscountRate from 0 to TimeHorizon included
    >>> from parameters import *
    >>> npv(MongDuong1)
    1.07676e+09 USD
    >>> npv(NinhBinh) 
    1.06588e+08 USD
    """
    value = zero_USD
    for year in range(time_horizon+1):
        value += net_cash_flow(plant, year) / (1+discount_rate)**year
    return value

if __name__ == "__main__":
    import doctest
    doctest.testmod()
