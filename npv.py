# Economic of co-firing in two power plants in Vietnam
#
#  NPV assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

"""Net present value assessment of a co-firing project
"""

from parameters import time_step, time_horizon, discount_rate, biomass_ratio
from parameters import electricity_tariff, tax_rate
from parameters import zero_kwh, zero_USD, zero_VND


def elec_sale(plant, year):
    """electricity sale refers to line 98 in Excel sheet
        this is only for the project

     In the first year, the project is not here yet so no sales:
     >>> from parameters import *
     >>> elec_sale(MongDuong1, 0)
     0 hr*kW
     >>> elec_sale(NinhBinh, 0)
     0 hr*kW

     From the second year onwards:
     >>> elec_sale(MongDuong1, 1)
     325 GW*hr
     >>> elec_sale(NinhBinh, 1)
     37.5 GW*hr
     
     Sales are assumed constant afterwards:
     >>> elec_sale(MongDuong1, 1) == elec_sale(MongDuong1, time_horizon)
     True
     >>> elec_sale(NinhBinh, 1) == elec_sale(NinhBinh, time_horizon)
     True
    """
    if year == 0:
        return zero_kwh
    else:
        return plant.generation * biomass_ratio * time_step


def cash_inflow(plant, year):
    """ Excel line 99 and 102
        This is only for the project

    In the first year, there is no sale so cash inflow is zero:
    >>> from parameters import *
    >>> l = cash_inflow(MongDuong1, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    >>> l = cash_inflow(NinhBinh, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD

    Cash inflow remain constant afterwards:
    >>> cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon)
    True
    >>> cash_inflow(NinhBinh, 1) == cash_inflow(NinhBinh, time_horizon)
    True

    Cash inflow on year one:
    >>> l = cash_inflow(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    17528.2 kUSD
    >>> l = cash_inflow(NinhBinh, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    2022.48 kUSD
    """
    return electricity_tariff * elec_sale(plant, year)


def cash_outflow(plant, year):
    """ This is only for the project

    Cash outflow year zero:
    >>> from parameters import *
    >>> l = cash_outflow(MongDuong1, 0)
    >>> l.display_unit = 'kUSD'
    >>> l
    2700 kUSD
    >>> l = cash_outflow(NinhBinh, 0)
    >>> l.display_unit = 'kUSD'
    >>> l
    500 kUSD

    Cash outflow from year one:
    >>> l = cash_outflow(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    15178.3 kUSD
    >>> l = cash_outflow(NinhBinh, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    2422.19 kUSD

    Cash outflow remain constant afterwards:
    >>> cash_outflow(MongDuong1, 1) == cash_outflow(MongDuong1, time_horizon)
    True
    >>> cash_outflow(NinhBinh, 1) == cash_outflow(NinhBinh, time_horizon)
    True
    """
    return (tot_capital_cost(plant, year) + fuel_cost(plant, year) +
            operation_maintenance_cost(plant, year) + income_tax(plant, year))


def tot_capital_cost(plant, year):
    """ We assume the plant is paid for coal at capacity design.
       this is only extra capital cost for the plant retrofitting for biomass co-firing  ??? Total
       This is only for the project

    Total capital cost is zero from year 1 afterwards:
    >>> from parameters import *
    >>> tot_capital_cost(MongDuong1, 1) == tot_capital_cost(MongDuong1, time_horizon) == zero_USD
    True
    >>> tot_capital_cost(NinhBinh, 1) == tot_capital_cost(NinhBinh, time_horizon) == zero_USD
    True

    Total capital cost on year zero:
    >>> l = tot_capital_cost(MongDuong1, 0)
    >>> l.display_unit = 'kUSD'
    >>> l
    2700 kUSD
    >>> l = tot_capital_cost(NinhBinh, 0)
    >>> l.display_unit = 'kUSD'
    >>> l
    500 kUSD
    """
    if year == 0:
        return plant.capital_cost * plant.capacity * biomass_ratio
    else:
        return zero_USD


def fuel_cost(plant, year):
    """Total expense on biomass

    No fuel cost on year zero:
    >>> from parameters import *
    >>> l = fuel_cost(MongDuong1, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    >>> l = fuel_cost(NinhBinh, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD

    Fuel cost remain constant:
    >>> fuel_cost(MongDuong1, 1) == fuel_cost(MongDuong1, time_horizon)
    True
    >>> fuel_cost(NinhBinh, 1) == fuel_cost(NinhBinh, time_horizon)
    True

    Fuel cost on year one:
    >>> l = fuel_cost(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    10704 kUSD
    >>> l = fuel_cost(NinhBinh, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    2035.99 kUSD
    """
    if year == 0:
        return zero_USD
    else:
        biomass_cost = plant.biomass_unit_cost * plant.biomass_required
        return biomass_cost * time_step


def operation_maintenance_cost(plant, year):
    """total expense for the cofiring project

    No O&M cost for co-firing on the first year:
    >>> from parameters import *
    >>> l = operation_maintenance_cost(MongDuong1, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    >>> l = operation_maintenance_cost(NinhBinh, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD

    O&M cost on year one:
    >>> l = operation_maintenance_cost(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    3690.96 kUSD
    >>> l = operation_maintenance_cost(NinhBinh, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    386.2 kUSD

    O&M cost remain constant from year 1 onwards:
    >>> operation_maintenance_cost(MongDuong1, 1) == operation_maintenance_cost(MongDuong1, time_horizon)
    True
    >>> operation_maintenance_cost(NinhBinh, 1) == operation_maintenance_cost(NinhBinh, time_horizon)
    True
    """
    if year == 0:
        return zero_USD
    else:
        fixed_om_cost = plant.fix_om_cost * plant.capacity * biomass_ratio * time_step
        variable_om_cost = plant.variable_om_cost * elec_sale(plant, year) 
        return fixed_om_cost + variable_om_cost


def income_tax(plant, year):
    """Corporate tax
    No income tax for co-firing on the first year:
    >>> from parameters import *
    >>> l = income_tax(MongDuong1, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    >>> l = income_tax(NinhBinh, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD

    Income tax on year 1:
    >>> l = income_tax(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    783.299 kUSD
    >>> l = income_tax(NinhBinh, 1)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD

    Income tax remain constant from year 1 onwards:
    >>> income_tax(MongDuong1, 1) == income_tax(MongDuong1, time_horizon)
    True
    >>> income_tax(NinhBinh, 1) == income_tax(NinhBinh, time_horizon)
    True
    """
    if year == 0:
        return zero_VND
    else:
# 0 dimension VND
        if tax_rate * earning_before_tax(plant, year) >  zero_VND:
            return tax_rate * earning_before_tax(plant, year)
        else:
            return zero_VND


def earning_before_tax(plant, year):
    """Amortizations not excluded (yet) from tax base

    No earning before tax for co-firing on the first year:
    >>> from parameters import *
    >>> l = earning_before_tax(MongDuong1, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    >>> l = earning_before_tax(NinhBinh, 0)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    
    Earning before tax on year 1:
    >>> l = earning_before_tax(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    3133.19 kUSD
    >>> l = earning_before_tax(NinhBinh, 1)
    >>> l.display_unit = 'USD'
    >>> l
    0 USD
    
    Earning before tax remain constant from year 1 onwards:
    >>> earning_before_tax(MongDuong1, 1) == earning_before_tax(MongDuong1, time_horizon)
    True
    >>> earning_before_tax(NinhBinh, 1) == earning_before_tax(NinhBinh, time_horizon)
    True
    """
    if year == 0:
        return zero_VND
    else:
        if (cash_inflow(plant, year) - fuel_cost(plant, year) - operation_maintenance_cost(plant, year)) > zero_VND:
            return (cash_inflow(plant, year) - fuel_cost(plant, year) - operation_maintenance_cost(plant, year))
        else:
            return zero_VND
    return zero_VND

def net_cash_flow(plant, year):
    """Cash flow of the co-firing project
    
    Net cash flow on year 0:
    >>> from parameters import *   
    >>> l = net_cash_flow(MongDuong1, 0)
    >>> l.display_unit = 'kUSD'
    >>> l
    -2700 kUSD
    >>> l = net_cash_flow(NinhBinh, 0)
    >>> l.display_unit = 'kUSD'
    >>> l
    -500 kUSD
    
    Net cash flow on year 1:
    >>> l = net_cash_flow(MongDuong1, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    2349.9 kUSD
    >>> l = net_cash_flow(NinhBinh, 1)
    >>> l.display_unit = 'kUSD'
    >>> l
    -399.71 kUSD
    
    Net cash flow remains constant from year 1 onwards:
    >>> net_cash_flow(MongDuong1, 1) == net_cash_flow(MongDuong1, time_horizon)
    True
    >>> net_cash_flow(NinhBinh, 1) == net_cash_flow(NinhBinh, time_horizon)
    True
    """
    return cash_inflow(plant, year) - cash_outflow(plant, year)


def npv(plant):
    """npv returns the Net Present Value of the project,
    discounted at DiscountRate from 0 to TimeHorizon included
    """
    value = zero_USD
    for year in range(time_horizon+1):
        value += net_cash_flow(plant, year) / (1+discount_rate)**year
    return value


if __name__ == "__main__":
    import doctest
    doctest.testmod()
