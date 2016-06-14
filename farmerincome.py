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

from parameters import winder_rental_cost, biomass_fix_cost, time_step


def farmer_income(plant):
    """ Extra income per hecta of rice cultivation for farmer from selling rice
        straw for co-firing after deducting the cost for renting straw winder

    >>> from parameters import *
    >>> l = farmer_income(MongDuong1)
    >>> l.display_unit = 'USD/ha/y'
    >>> l
    168.842 USD/(ha*y)
    >>> l = farmer_income(NinhBinh)
    >>> l.display_unit = 'USD/ha/y'
    >>> l
    172.382 USD/(ha*y)
    """
    return bm_sell_revenue(plant) - winder_rental_cost / time_step


def bm_sell_revenue(plant):
    """ Revenue per hecta of rice cultivation for farmer from selling rice straw

    >>> from parameters import *
    >>> l = bm_sell_revenue(MongDuong1)
    >>> l.display_unit = 'USD/ha/y'
    >>> l
    208.842 USD/(ha*y)
    >>> l = bm_sell_revenue(NinhBinh)
    >>> l.display_unit = 'USD/ha/y'
    >>> l
    212.382 USD/(ha*y)
    """
    return plant.biomass_yeild * biomass_fix_cost


def total_income_benefit(plant):
    """ Total benefit for the farmers from having extra income selling
        rice straw to the plant for co-firing

    >>> from parameters import *
    >>> l = total_income_benefit(MongDuong1)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    7805.24 kUSD/y
    >>> l = total_income_benefit(NinhBinh)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    1613.84 kUSD/y
    """
    return farmer_income(plant) * plant.rice_cultivation_area

if __name__ == "__main__":
    import doctest
    doctest.testmod()
