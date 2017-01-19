# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Assessment of extra income for farmer from co-firing projects"""

from parameters import winder_rental_cost, biomass_fix_cost
from biomassrequired import cultivation_area
from units import time_step, print_with_unit


def farmer_income(plant):
    """ Extra income per hecta of rice cultivation for farmer from selling rice
        straw for co-firing after deducting the cost for renting straw winder

    >>> from parameters import *
    >>> print_with_unit(farmer_income(MongDuong1), 'USD/ha/y')
    168.842 USD/(ha*y)
    >>> print_with_unit(farmer_income(NinhBinh), 'USD/ha/y')
    172.382 USD/(ha*y)
    """
    return bm_sell_revenue(plant) - winder_rental_cost / time_step


def bm_sell_revenue(plant):
    """ Revenue per hecta of rice cultivation for farmer from selling rice straw

    >>> from parameters import *
    >>> print_with_unit(bm_sell_revenue(MongDuong1), 'USD/ha/y')
    208.842 USD/(ha*y)
    >>> print_with_unit(bm_sell_revenue(NinhBinh), 'USD/ha/y')
    212.382 USD/(ha*y)
    """
    return plant.biomass_yield * biomass_fix_cost


def total_income_benefit(plant):
    """ Total benefit for the farmers from having extra income selling
        rice straw to the plant for co-firing

    >>> from parameters import *
    >>> print_with_unit(total_income_benefit(MongDuong1), 'kUSD/y')
    6821 kUSD/y
    >>> print_with_unit(total_income_benefit(NinhBinh), 'kUSD/y')
    1207.17 kUSD/y
    """
    return farmer_income(plant) * cultivation_area(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    