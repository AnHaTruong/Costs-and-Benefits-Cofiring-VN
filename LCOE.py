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

from parameters import discount_rate, time_horizon
from parameters import biomass_heat_value, h_per_yr


def cap_rec_factor():
    """Calcuate the capital recovery factor """
    return ((discount_rate * (1 + discount_rate)**time_horizon) /
            ((1 + discount_rate)**time_horizon - 1))


def bm_unit_cost_mj(plant):
    """return the biomass unit cost in USD/MJ"""
    return plant.biomass_unit_cost / biomass_heat_value


def lcoe_cap_return(plant):
    """Contribution of capital cost in lcoe"""
    return plant.capital_cost * cap_rec_factor()/h_per_yr / plant.capacity_factor
    

def lcoe_fix_om(plant):
    """Contribution of fix O&M cost in lcoe """
    return plant.fix_om_cost/(h_per_yr*plant.capacity_factor)


def lcoe_bm_cost(plant):
    """Contribution of fuel cost in lcoe"""
    return bm_unit_cost_mj(plant) * plant.heat_rate


def lcoe_variable_om(plant):
    """Contribution of variable O&M cost in lcoe"""
    return plant.variable_om_cost


def lcoe(plant):
    """calcuate the levelized cost of electricity for co-firing project"""
    return (lcoe_cap_return(plant)
            + lcoe_fix_om(plant)
            + lcoe_bm_cost(plant)
            + lcoe_variable_om(plant)
           )
