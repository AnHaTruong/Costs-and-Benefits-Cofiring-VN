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
    >>> farmer_income(MongDuong1)
    3.71453e+06 mol/(ha*y)
    >>> farmer_income(NinhBinh)
    <Quantity(172.382, 'USD / hectare / year')>
    """
    return bm_sell_revenue(plant) - winder_rental_cost / time_step


def bm_sell_revenue(plant):
    """ Revenue per hecta of rice cultivation for farmer from selling rice straw

    >>> from parameters import *
    >>> bm_sell_revenue(MongDuong1)
    <Quantity(208.8423, 'USD / hectare / year')>
    >>> bm_sell_revenue(NinhBinh)
    <Quantity(212.382, 'USD / hectare / year')>
    """
    return plant.biomass_yeild * biomass_fix_cost


def total_income_benefit(plant):
    """ Total benefit for the farmers from having extra income selling
        rice straw to the plant for co-firing

    >>> from parameters import *
    >>> total_income_benefit(MongDuong1)
    <Quantity(7805241.8444, 'USD / year')>
    >>> total_income_benefit(NinhBinh)
    <Quantity(1613840.284, 'USD / year')>
    """
    return farmer_income(plant) * plant.rice_cultivation_area

if __name__ == "__main__":
    import doctest
    doctest.testmod()
