# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Calculation of overall cost-benefit of co-firing added up for the same
    number of years as used for NPV calculation
"""

from init import zero_USD, time_horizon, time_step
from parameters import discount_rate
from health import total_health_benefit
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit
from job import total_job_benefit
import natu.numpy as np


def benefit_add_up(func, plant):
    """return the present value of cumulative benefits of co-firing
    discounted at DiscountRate from 0 to TimeHorizon included
    """
    value = zero_USD
    for year in range(time_horizon + 1):
        value += (func(plant) * time_step) / (1 + discount_rate)**year
    value.display_unit = 'kUSD'
    return value


def new_benefit_add_up(func, plant, cofiringplant):
    """return the present value of cumulative benefits of co-firing
    discounted at DiscountRate from 0 to TimeHorizon included
    """
    value = zero_USD
    for year in range(time_horizon + 1):
        value += (func(plant, cofiringplant) * time_step) / (1 + discount_rate)**year
    value.display_unit = 'kUSD'
    return value


def total_benefit_addup(plant, cofiringplant):
    """Total benefit of co-firing added up for the same number of year as used
       in NPV calculation discounted at same DiscountRate
    """
    return (new_benefit_add_up(total_health_benefit, plant, cofiringplant)
            + benefit_add_up(total_income_benefit, plant)
            + new_benefit_add_up(emission_reduction_benefit, plant, cofiringplant)
            + new_benefit_add_up(total_job_benefit, plant, cofiringplant)
            )


def benefit_add_up_new(func):
    value = zero_USD
    for year in range(time_horizon + 1):
        value += (func) * time_step / (1 + discount_rate)**year
    value.display_unit = 'kUSD'
    return value

if __name__ == "__main__":
    import doctest
    doctest.testmod()
