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
     <Quantity(0, 'kilowatt_hour')>
     >>> elec_sale(NinhBinh, 0)
     <Quantity(0, 'kilowatt_hour')>
     
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
    >>> cash_inflow(MongDuong1, 0)
    <Quantity(0.0, 'VND')>
    >>> cash_inflow(NinhBinh, 0)
    <Quantity(0.0, 'VND')>
    """
    return elec_sale(plant, year) * electricity_tariff


def cash_outflow(plant, year):
    """ This is only for the project
    
    """
    return (tot_capital_cost(plant, year) + fuel_cost(plant, year) +
            operation_maintenance_cost(plant, year) + income_tax(plant, year))


def tot_capital_cost(plant, year):
    """ We assume the plant is paid for coal at capacity design.
       this is only extra capital cost for the biomass co-firing  ??? Total
       This is only for the project
       
    Total capital cost is zero from year 1 afterwards:
    >>> from parameters import *    
    >>> tot_capital_cost(MongDuong1, 1) == tot_capital_cost(MongDuong1, time_horizon) == 0
    True
    >>> tot_capital_cost(NinhBinh, 1) == tot_capital_cost(NinhBinh, time_horizon) == 0
    True
    """
    if year == 0:
        return plant.capacity * plant.capital_cost * biomass_ratio
    else:
        return zero_USD


def fuel_cost(plant, year):
    """total expense on biomass
    
    no fuel cost on year zero:
    >>> from parameters import *
    >>> fuel_cost(MongDuong1, 0)
    <Quantity(0, 'USD')>
    >>> fuel_cost(NinhBinh, 0)
    <Quantity(0, 'USD')>
    
    fuel cost remain constant:
     >>> fuel_cost(MongDuong1, 1) == fuel_cost(MongDuong1, time_horizon)
     True
     >>> fuel_cost(NinhBinh, 1) == fuel_cost(NinhBinh, time_horizon)
     True
    """
    if year == 0:
        return zero_USD
    else:
        biomass_cost = plant.biomass_required * plant.biomass_unit_cost
        return biomass_cost * time_step


def operation_maintenance_cost(plant, year):
    """total expense for the cofiring project
    
    No O&M cost for co-firing on the first year:
    >>> from parameters import *
    >>> operation_maintenance_cost(MongDuong1, 0)
    <Quantity(0, 'USD')>
    >>> operation_maintenance_cost(NinhBinh, 0)
    <Quantity(0, 'USD')>
    
    """
    if year == 0:
        return zero_USD
    else:
        fixed_om_cost = plant.capacity * plant.fix_om_cost * biomass_ratio * time_step
        variable_om_cost = elec_sale(plant, year) * plant.variable_om_cost
        return fixed_om_cost + variable_om_cost


def income_tax(plant, year):
    """Corporate tax
    No income tax for co-firing on the first year:
    >>> from parameters import *
    >>> income_tax(MongDuong1, 0)
    <Quantity(0, 'VND')>
    >>> income_tax(NinhBinh, 0)
    <Quantity(0, 'VND')>
    """
    if year == 0:
        return zero_VND
    else:
        return tax_rate * earning_before_tax(plant, year)


def earning_before_tax(plant, year):
    """Amortizations not excluded (yet) from tax base"""
    if year == 0:
        return zero_VND
    else:
        return (cash_inflow(plant, year) - fuel_cost(plant, year) -
                operation_maintenance_cost(plant, year))


def net_cash_flow(plant, year):
    """Cash flow of the co-firing project"""
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
