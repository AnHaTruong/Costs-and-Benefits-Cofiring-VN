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

     From the second year onwards:
     >>> elec_sale(MongDuong1, 1)
     <Quantity(325.0, 'gigawatt_hour')>
     >>> elec_sale(NinhBinh, 1)
     <Quantity(37.5, 'gigawatt_hour')>

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

    Cash inflow remain constant afterwards:
    >>> cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon)
    True
    >>> cash_inflow(NinhBinh, 1) == cash_inflow(NinhBinh, time_horizon)
    True

    Cash inflow on year one:
    >>> cash_inflow(MongDuong1, 1)
    <Quantity(376382.49999999994, 'VND * gigawatt_hour / kilowatt_hour')>
    >>> cash_inflow(NinhBinh, 1)
    <Quantity(43428.75, 'VND * gigawatt_hour / kilowatt_hour')>
    """
    return electricity_tariff * elec_sale(plant, year)


def cash_outflow(plant, year):
    """ This is only for the project

    Cash outflow year zero:
    >>> from parameters import *
    >>> cash_outflow(MongDuong1, 0)
    <Quantity(2700.0, 'USD * megawatt / kilowatt')>
    >>> cash_outflow(NinhBinh, 0)
    <Quantity(500.0, 'USD * megawatt / kilowatt')>

    Cash outflow from year one:
    >>> cash_outflow(MongDuong1, 1)
    <Quantity(15178279.018584013, 'USD')>
    >>> cash_outflow(NinhBinh, 1)
    <Quantity(2422192.002333168, 'USD')>

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
       this is only extra capital cost for the biomass co-firing  ??? Total
       This is only for the project

    Total capital cost is zero from year 1 afterwards:
    >>> from parameters import *
    >>> tot_capital_cost(MongDuong1, 1) == tot_capital_cost(MongDuong1, time_horizon) == 0
    True
    >>> tot_capital_cost(NinhBinh, 1) == tot_capital_cost(NinhBinh, time_horizon) == 0
    True

    Total capital cost on year zero:
    >>> tot_capital_cost(MongDuong1, 0)
    <Quantity(2700.0, 'USD * megawatt / kilowatt')>
    >>> tot_capital_cost(NinhBinh, 0)
    <Quantity(500.0, 'USD * megawatt / kilowatt')>
    """
    if year == 0:
        return plant.capital_cost * plant.capacity * biomass_ratio
    else:
        return zero_USD


def fuel_cost(plant, year):
    """Total expense on biomass

    No fuel cost on year zero:
    >>> from parameters import *
    >>> fuel_cost(MongDuong1, 0)
    <Quantity(0, 'USD')>
    >>> fuel_cost(NinhBinh, 0)
    <Quantity(0, 'USD')>

    Fuel cost remain constant:
    >>> fuel_cost(MongDuong1, 1) == fuel_cost(MongDuong1, time_horizon)
    True
    >>> fuel_cost(NinhBinh, 1) == fuel_cost(NinhBinh, time_horizon)
    True

    Fuel cost on year one:
    >>> fuel_cost(MongDuong1, 1)
    <Quantity(10704020.385666, 'USD')>
    >>> fuel_cost(NinhBinh, 1)
    <Quantity(2035992.0023331677, 'USD')>
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
    >>> operation_maintenance_cost(MongDuong1, 0)
    <Quantity(0, 'USD')>
    >>> operation_maintenance_cost(NinhBinh, 0)
    <Quantity(0, 'USD')>

    O&M cost on year one:
    >>> operation_maintenance_cost(MongDuong1, 1)
    <Quantity(3690.96, 'USD * megawatt / kilowatt')>
    >>> operation_maintenance_cost(NinhBinh, 1)
    <Quantity(386.20000000000005, 'USD * megawatt / kilowatt')>

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
    >>> income_tax(MongDuong1, 0)
    <Quantity(0, 'VND')>
    >>> income_tax(NinhBinh, 0)
    <Quantity(0, 'VND')>

    Income tax on year 1:
    >>> income_tax(MongDuong1, 1)
    <Quantity(16819.771544648487, 'VND * gigawatt_hour / kilowatt_hour')>
    >>> income_tax(NinhBinh, 1)
    <Quantity(0, 'VND')>

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
    >>> earning_before_tax(MongDuong1, 0)
    <Quantity(0, 'VND')>
    >>> earning_before_tax(NinhBinh, 0)
    <Quantity(0, 'VND')>

    Earning before tax on year 1:
    >>> earning_before_tax(MongDuong1, 1)
    <Quantity(67279.08617859395, 'VND * gigawatt_hour / kilowatt_hour')>
    >>> earning_before_tax(NinhBinh, 1)
    <Quantity(0, 'VND')>
    
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
    >>> net_cash_flow(MongDuong1, 0)
    <Quantity(-57977100000.0, 'VND')>
    >>> net_cash_flow(NinhBinh, 0)
    <Quantity(-10736500000.0, 'VND')>
    
    Net cash flow on year 1:
    >>> net_cash_flow(MongDuong1, 1)
    <Quantity(50459.31463394547, 'VND * gigawatt_hour / kilowatt_hour')>
    >>> net_cash_flow(NinhBinh, 1)
    <Quantity(-8582.978866100115, 'VND * gigawatt_hour / kilowatt_hour')>
    
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
