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

from parameters import time_horizon, discount_rate, biomass_ratio
from parameters import electricity_tariff_USD, tax_rate


def npv(cash_flow):
    """npv returns the Net Present Value of the cashflow(year),
    discounted at DiscountRate from 0 to TimeHorizon included
    """
    value = 0
    for year in range(time_horizon+1):
        value += cash_flow(year) / (1+discount_rate)**year
    return value


def elec_sale_kwh(plant, year):
    """electricity sale refers to line 98 in Excel sheet
        this is only for the project
    """
    if year == 0:
        return 0
    else:
        return plant.generation * biomass_ratio


def cash_inflow(plant, year):
    """ Excel line 99 and 102
        This is only for the project
    """
    return elec_sale_kwh(plant, year) * electricity_tariff_USD


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
        return 0


def fuel_cost(plant, year):
    """total expense on biomass"""
    if year == 0:
        return 0
    else:
        biomass_cost = plant.biomass_required * plant.biomass_unit_cost
        return biomass_cost


def operation_maintenance_cost(plant, year):
    """total expense for the cofiring project"""
    fixed_om_cost = plant.capacity * plant.fix_om_cost * biomass_ratio
    variable_om_cost = elec_sale_kwh(plant, year) * plant.variable_om_cost
    return fixed_om_cost + variable_om_cost


def income_tax(plant, year):
    """Corporate tax"""
    return tax_rate * earning_before_tax(plant, year)


def earning_before_tax(plant, year):
    """Amortizations not excluded (yet) from tax base"""
    return (cash_inflow(plant, year) - fuel_cost(plant, year) -
            operation_maintenance_cost(plant, year))


def net_cash_flow(plant, year):
    """Cash flow of the co-firing project"""
    return cash_inflow(plant, year) - cash_outflow(plant, year)
