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
from units import zero_kwh
from natu.numpy import npv


def discount(func, plant, time, rate):
    value = [func(plant, year) for year in range (time + 1)]
    return npv(rate, value)
# FIXME: Use a common discount function everywhere


def lcoe_power_gen(plant):
    """ Sum of electricity generation over Time_Horizon

    """
    value = zero_kwh
    for year in range(time_horizon+1):
            value += plant.elec_sale / (1+discount_rate)**year
    return value


if __name__ == "__main__":
    import doctest
    doctest.testmod()
