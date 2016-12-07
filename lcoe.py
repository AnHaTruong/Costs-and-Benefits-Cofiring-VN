# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity(LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""LCOE assessment of a co-firing project"""


from parameters import discount_rate, time_horizon, time_step, zero_USD
from parameters import h_per_yr, MongDuong1, NinhBinh, zero_kwh
from npv import tot_capital_cost, fuel_cost_coal, fuel_cost_biomass
from npv import operation_maintenance_cost, income_tax, elec_sale


def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value


def lcoe_investment(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(lcoe_investment, MongDuong1, 'kUSD')
    2700 kUSD
    >>> print_with_unit(lcoe_investment, NinhBinh, 'kUSD')
    500 kUSD
    """
    return tot_capital_cost(plant, 0)



def lcoe_fuel_coal(plant):
    """ Present value of cumilative coal cost over Time_Horizon discounted at Discount_Rate

    >>> from parameters import *
    >>> print_with_unit(lcoe_fuel_coal, MongDuong1, 'kUSD')
    1.22312e+06 kUSD
    >>> print_with_unit(lcoe_fuel_coal, NinhBinh, 'kUSD')
    297341 kUSD
    """
    value = zero_USD
    for year in range(time_horizon+1):
            value += fuel_cost_coal(plant, year) / (1+discount_rate)**year
    return value


def lcoe_fuel_biomass(plant):
    """ Present value of cumilative biomass cost over Time_Horizon discounted at Discount_Rate

    >>> from parameters import *
    >>> print_with_unit(lcoe_fuel_biomass, MongDuong1, 'kUSD')
    104817 kUSD
    >>> print_with_unit(lcoe_fuel_biomass, NinhBinh, 'kUSD')
    19141.1 kUSD
    """
    value = zero_USD
    for year in range(time_horizon+1):
            value += fuel_cost_biomass(plant, year) / (1+discount_rate)**year
    return value


def lcoe_om(plant):
    """ Present value of cumilative O&M cost over Time_Horizon discounted at Discount_Rate

    >>> from parameters import *
    >>> print_with_unit(lcoe_om, MongDuong1, 'kUSD')
    588089 kUSD
    >>> print_with_unit(lcoe_om, NinhBinh, 'kUSD')
    61131 kUSD
    """

    value = zero_USD
    for year in range(time_horizon+1):
            value += operation_maintenance_cost(plant, year) / (1+discount_rate)**year
    return value


def lcoe_tax(plant):
    """ Present value of cumilative tax over Time_Horizon discounted at Discount_Rate

    >>> from parameters import *
    >>> print_with_unit(lcoe_tax, MongDuong1, 'kUSD')
    359238 kUSD
    >>> print_with_unit(lcoe_tax, NinhBinh, 'kUSD')
    35588.1 kUSD
    """
    value = zero_USD
    for year in range(time_horizon+1):
            value += income_tax(plant, year) / (1+discount_rate)**year
    return value


def lcoe_cost(plant):
    """ Sum of costs over Time_Horizon discounted at Discount_Rate

    >>> from parameters import *
    >>> print_with_unit(lcoe_cost, MongDuong1, 'kUSD')
    2.27796e+06 kUSD
    >>> print_with_unit(lcoe_cost, NinhBinh, 'kUSD')
    413701 kUSD
    """
    return (lcoe_investment(plant) +
            lcoe_fuel_coal(plant) +
            lcoe_fuel_biomass(plant) +
            lcoe_om(plant) +
            lcoe_tax(plant)
           )


def lcoe_power_gen(plant):
    """ Sum of electricity generation over Time_Horizon

    >>> from parameters import *
    >>> print_with_unit(lcoe_power_gen, MongDuong1, 'GWh')
    60290.2 GWh
    >>> print_with_unit(lcoe_power_gen, NinhBinh, 'GWh')
    6956.56 GWh
    """
    value = zero_kwh
    for year in range(time_horizon+1):
            value += elec_sale(plant, year) / (1+discount_rate)**year
    return value


def lcoe(plant):
    """ This LCOE calculation does not include the initial investment cost of the plant
    It only takes into account the investment cost for co-firing
    
    >>> from parameters import *
    >>> print_with_unit(lcoe, MongDuong1, 'USD/kWh')
    0.0377833 USD/kWh
    >>> print_with_unit(lcoe, NinhBinh, 'USD/kWh')
    0.0594692 USD/kWh
    """
    return lcoe_cost(plant) / lcoe_power_gen(plant)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
