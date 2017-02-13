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

from parameters import biomass_ratio, tax_rate, discount_rate, depreciation_period
from units import time_horizon, zero_USD, zero_VND, time_step
from biomassrequired import biomass_required
from biomasscost import bm_unit_cost
from coalsaved import coal_saved


def cash_inflow(plant, year):
    """

    Cash inflow remain constant :
    >>> from parameters import *
    >>> cash_inflow(MongDuong1, 1) == cash_inflow(MongDuong1, time_horizon)
    True
    >>> cash_inflow(NinhBinh, 1) == cash_inflow(NinhBinh, time_horizon)
    True

    """
    return plant.electricity_tariff * plant.elec_sale


def cash_outflow(plant, year):
    """ This is for the whole plant

    """
    return (tot_capital_cost(plant, year) + fuel_cost(plant, year) +
            operation_maintenance_cost(plant, year) + income_tax(plant, year))


def tot_capital_cost(plant, year):
    """ We assume the plant is paid for coal at capacity design.
       this is only extra capital cost for the plant retrofitting for biomass co-firing

    Total capital cost is zero from year 1 afterwards:
    >>> from parameters import *
    >>> tot_capital_cost(MongDuong1, 1) == tot_capital_cost(MongDuong1, time_horizon) == zero_USD
    True
    >>> tot_capital_cost(NinhBinh, 1) == tot_capital_cost(NinhBinh, time_horizon) == zero_USD
    True
    """
    if year == 0:
        return plant.capital_cost * plant.capacity * biomass_ratio
    else:
        return zero_USD


def fuel_cost_coal(plant, year):
    """Fuel expense on coal

    """
    if year == 0:
        return plant.base_coal_consumption * plant.coal_price * time_step
    else:
        return plant.coal_price * (plant.base_coal_consumption - coal_saved(plant)) * time_step


def fuel_cost_biomass(plant, year):
    """Fuel expense on biomass
    """
    if year == 0:
        return zero_USD
    else:
        return bm_unit_cost(plant) * biomass_required(plant) * time_step


def fuel_cost(plant, year):
    """Total expense on fuel cost including both coal and  biomass

    Fuel cost remain constant from year 1 onward:
    >>> from parameters import *
    >>> fuel_cost(MongDuong1, 1) == fuel_cost(MongDuong1, time_horizon)
    True
    >>> fuel_cost(NinhBinh, 1) == fuel_cost(NinhBinh, time_horizon)
    True
    """
    return fuel_cost_coal(plant, year) + fuel_cost_biomass(plant, year)


def operation_maintenance_cost(plant, year):
    """total expense for the plant

    O&M cost remain constant from year 1 onwards:
    >>> from parameters import *
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
    Earning before tax is the cash inflow exclude all costs
    """
    return (cash_inflow(plant, year) -
            fuel_cost(plant, year) -
            operation_maintenance_cost(plant, year) -
            amortization(plant, year)
            )


def net_cash_flow(plant, year):
    """Cash flow of the plant

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
