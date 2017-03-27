# encoding: utf-8
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
import natu.numpy as np
from init import time_horizon, display_as
from parameters import discount_rate
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit, total_health_benefit
from job import total_job_benefit


def benefit_add_up(func, plant, cofiringplant):
    """return the present value of cumulative benefits of co-firing
       discounted at DiscountRate from 1 to TimeHorizon included
    """
    r = 1 / (1 + discount_rate)
    value = func(plant, cofiringplant) * (r - r**(time_horizon + 1)) / (1 - r)
    return display_as(value, 'kUSD')


def job_benefit_add_up(plant, cofiringplant):
    return (np.npv(discount_rate, total_job_benefit(plant, cofiringplant)) -
            total_job_benefit(plant, cofiringplant)[0]
            )


def total_benefit_addup(plant, cofiringplant):
    """Total benefit of co-firing added up for the same number of year as used
       in NPV calculation discounted at same DiscountRate
    """
    return (benefit_add_up(total_health_benefit, plant, cofiringplant)
            + benefit_add_up(total_income_benefit, plant, cofiringplant)
            + benefit_add_up(emission_reduction_benefit, plant, cofiringplant)
            + job_benefit_add_up(plant, cofiringplant)
            )
