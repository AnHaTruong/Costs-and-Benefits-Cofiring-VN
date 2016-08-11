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
from biomasscost import bm_unit_cost
from biomassrequired import plant_efficency_bm


def capacity_factor(plant):
    """
    >>> capacity_factor(MongDuong1)
    0.687045492981566
    >>> capacity_factor(NinhBinh)
    0.8561643835616437
    """
    return plant.generation / (plant.capacity * h_per_yr) * time_step


def heat_rate(plant):
    """
    >>> heat_rate(MongDuong1)
    2.59107274137779
    >>> heat_rate(NinhBinh)
    4.624707211364663
    """
    return (1/plant_efficency_bm(plant))


def cap_rec_factor():
    """Calcuate the capital recovery factor

    >>> from parameters import *
    >>> cap_rec_factor()
    0.10781189728784245
    """
    return ((discount_rate * (1 + discount_rate)**time_horizon) /
            ((1 + discount_rate)**time_horizon - 1))


def print_with_unit(func, plant, unit):
    l = func(plant)
    l.display_unit = unit
    return l


def lcoe_cap_return(plant):
    """Contribution of capital cost in lcoe

    >>> from parameters import *
    >>> print_with_unit(lcoe_cap_return, MongDuong1, 'USD/hr/kW')
    0.000895668 USD/(hr*kW)
    >>> print_with_unit(lcoe_cap_return, NinhBinh, 'USD/hr/kW')
    0.00143749 USD/(hr*kW)
    """
    return plant.capital_cost * cap_rec_factor()/h_per_yr / capacity_factor(plant)


def lcoe_fix_om(plant):
    """Contribution of fix O&M cost in lcoe

    >>> from parameters import *
    >>> print_with_unit(lcoe_fix_om, MongDuong1, 'USD/hr/kW')
    0.0053568 USD/(hr*kW)
    >>> print_with_unit(lcoe_fix_om, NinhBinh, 'USD/hr/kW')
    0.00429867 USD/(hr*kW)
    """
    return plant.fix_om_cost/(h_per_yr * capacity_factor(plant)) * time_step


def lcoe_bm_cost(plant):
    """Contribution of fuel cost in lcoe

    >>> from parameters import *
    >>> print_with_unit(lcoe_bm_cost, MongDuong1, 'USD/hr/kW')
    0.0330897 USD/(hr*kW)
    >>> print_with_unit(lcoe_bm_cost, NinhBinh, 'USD/hr/kW')
    0.0543633 USD/(hr*kW)
    """
    return bm_unit_cost(plant) * heat_rate(plant) / biomass_heat_value


def lcoe_variable_om(plant):
    """Contribution of variable O&M cost in lcoe

    >>> from parameters import *
    >>> print_with_unit(lcoe_variable_om, MongDuong1, 'USD/hr/kW')
    0.006 USD/(hr*kW)
    >>> print_with_unit(lcoe_variable_om, NinhBinh, 'USD/hr/kW')
    0.006 USD/(hr*kW)
    """
    return plant.variable_om_cost


def lcoe(plant):
    """Calculate the levelized cost of electricity for co-firing project

    >>> from parameters import *
    >>> print_with_unit(lcoe, MongDuong1, 'USD/hr/kW')
    0.0453421 USD/(hr*kW)
    >>> print_with_unit(lcoe, NinhBinh, 'USD/hr/kW')
    0.0660994 USD/(hr*kW)
    """
    return (lcoe_cap_return(plant)
            + lcoe_fix_om(plant)
            + lcoe_bm_cost(plant)
            + lcoe_variable_om(plant)
           )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
