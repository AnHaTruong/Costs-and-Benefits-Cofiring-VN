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

from parameters import discount_rate, time_horizon, time_step
from parameters import h_per_yr, biomass_heat_value


def cap_rec_factor():
    """Calcuate the capital recovery factor

    >>> from parameters import *
    >>> cap_rec_factor()
    <Quantity(0.10781189728784245, 'dimensionless')>
    """
    return ((discount_rate * (1 + discount_rate)**time_horizon) /
            ((1 + discount_rate)**time_horizon - 1))


def lcoe_cap_return(plant):
    """Contribution of capital cost in lcoe

    >>> from parameters import *
    >>> lcoe_cap_return(MongDuong1)
    <Quantity(0.0008956680697759168, 'USD / hour / kilowatt')>
    >>> lcoe_cap_return(NinhBinh)
    <Quantity(0.0014374919638379057, 'USD / hour / kilowatt')>
    """
    return plant.capital_cost * cap_rec_factor()/h_per_yr / plant.capacity_factor


def lcoe_fix_om(plant):
    """Contribution of fix O&M cost in lcoe

    >>> from parameters import *
    >>> lcoe_fix_om(MongDuong1)
    <Quantity(0.005356799999999969, 'USD / hour / kilowatt')>
    >>> lcoe_fix_om(NinhBinh)
    <Quantity(0.004298666666666686, 'USD / hour / kilowatt')>
    """
    return plant.fix_om_cost/(h_per_yr * plant.capacity_factor) * time_step


def lcoe_bm_cost(plant):
    """Contribution of fuel cost in lcoe

    >>> from parameters import *
    >>> lcoe_bm_cost(MongDuong1)
    <Quantity(32.935472378176826, 'USD * kilogram / kilowatt_hour / metric_ton')>
    >>> lcoe_bm_cost(NinhBinh)
    <Quantity(54.29312006221783, 'USD * kilogram / kilowatt_hour / metric_ton')>
    """
    return (plant.biomass_unit_cost / biomass_heat_value) * plant.heat_rate


def lcoe_variable_om(plant):
    """Contribution of variable O&M cost in lcoe

    >>> from parameters import *
    >>> lcoe_variable_om(MongDuong1)
    <Quantity(0.006, 'USD / kilowatt_hour')>
    >>> lcoe_variable_om(NinhBinh)
    <Quantity(0.006, 'USD / kilowatt_hour')>
    """
    return plant.variable_om_cost


def lcoe(plant):
    """Calculate the levelized cost of electricity for co-firing project

    >>> from parameters import *
    >>> l = lcoe(MongDuong1)
    >>> l.display_unit = 'USD/(hr*kW)'
    >>> l
    0.0451879 USD/(hr*kW)
    >>> l = lcoe(NinhBinh)
    >>> l.display_unit = 'USD/(hr*kW)'
    >>> l
    0.0660293 USD/(hr*kW)
    """
    return (lcoe_cap_return(plant)
            + lcoe_fix_om(plant)
            + lcoe_bm_cost(plant)
            + lcoe_variable_om(plant)
           )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
