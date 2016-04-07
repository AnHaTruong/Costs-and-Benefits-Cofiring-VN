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
    """
    if year == 0:
        return zero_kwh
    else:
        return plant.generation * biomass_ratio * time_step


def cash_inflow(plant, year):
    """ Excel line 99 and 102
        This is only for the project
    """
    return elec_sale(plant, year) * electricity_tariff


def cash_outflow(plant, year):
    """This is only for the project"""
    return (tot_capital_cost(plant, year) + fuel_cost(plant, year) +
            operation_maintenance_cost(plant, year) + income_tax(plant, year))


def tot_capital_cost(plant, year):
    """ We assume the plant is paid for coal at capacity design.
       this is only extra capital cost for the biomass co-firing  ??? Total
       This is only for the project
    """
    if year == 0:
        return plant.capacity * plant.capital_cost * biomass_ratio
    else:
        return zero_USD


def fuel_cost(plant, year):
    """total expense on biomass"""
    if year == 0:
        return zero_USD
    else:
        biomass_cost = plant.biomass_required * plant.biomass_unit_cost
        return biomass_cost * time_step


def operation_maintenance_cost(plant, year):
    """total expense for the cofiring project"""
    if year == 0:
        return zero_USD
    else:
        fixed_om_cost = plant.capacity * plant.fix_om_cost * biomass_ratio * time_step
        variable_om_cost = elec_sale(plant, year) * plant.variable_om_cost
        return fixed_om_cost + variable_om_cost


def income_tax(plant, year):
    """Corporate tax"""
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
