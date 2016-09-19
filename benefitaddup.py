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


from parameters import zero_USD, time_horizon, discount_rate, time_step
from health import total_health_benefit
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit
from job import total_job_benefit


def print_with_unit(func, unit):
    """ Display the desired unit on Tables"""
    value = func
    value.display_unit = unit
    return value


def benefit_add_up(func, plant):
    """return the present value of cumulative benefits of co-firing 
    discounted at DiscountRate from 0 to TimeHorizon included
    
    >>> from parameters import *
    >>> print_with_unit(benefit_add_up(total_health_benefit, MongDuong1), 'kUSD')
    8814.49 kUSD
    >>> print_with_unit(benefit_add_up(total_income_benefit, MongDuong1), 'kUSD')
    80201.9 kUSD
    >>> print_with_unit(benefit_add_up(emission_reduction_benefit, MongDuong1), 'kUSD')
    331.233 kUSD
    >>> print_with_unit(benefit_add_up(total_job_benefit, MongDuong1), 'kUSD')
    4371.07 kUSD
    >>> print_with_unit(benefit_add_up(total_health_benefit, NinhBinh), 'kUSD')
    11630.9 kUSD
    >>> print_with_unit(benefit_add_up(total_income_benefit, NinhBinh), 'kUSD')
    16582.4 kUSD
    >>> print_with_unit(benefit_add_up(emission_reduction_benefit, NinhBinh), 'kUSD')
    71.3586 kUSD
    >>> print_with_unit(benefit_add_up(total_job_benefit, NinhBinh), 'kUSD')
    839.595 kUSD
    """
    value = zero_USD
    for year in range(time_horizon+1):
        value += (func(plant) *time_step) / (1+discount_rate)**year
    return value


def total_benefit_addup(plant):
    """Total benefit of co-firing added up for the same number of year as used
       in NPV calculation discounted at same DiscountRate
       
    >>> from parameters import *
    >>> print_with_unit(total_benefit_addup(MongDuong1), 'kUSD')
    93718.7 kUSD
    >>> print_with_unit(total_benefit_addup(NinhBinh), 'kUSD')
    29124.3 kUSD
    """
    return (benefit_add_up(total_health_benefit, plant) +
            benefit_add_up(total_income_benefit, plant) +
            benefit_add_up(emission_reduction_benefit, plant) +
            benefit_add_up(total_job_benefit, plant)
            )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    