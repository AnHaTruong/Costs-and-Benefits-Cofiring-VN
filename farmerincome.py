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

from parameters import winder_rental_cost, straw


def farmer_income(cofireplant):
    """ Extra income per hectare of rice cultivation for farmer from selling rice
        straw for co-firing after deducting the cost for renting straw winder
    """
    return bm_sell_revenue(cofireplant) - winder_rental_cost


def bm_sell_revenue(cofireplant):
    """ Revenue per hecta of rice cultivation for farmer from selling rice straw"""

    return cofireplant.straw_supply.average_straw_yield * straw.price


def cultivation_area(cofireplant):
    """ Area of rice cultivation needed to supply enough straw for co-firing"""
    return cofireplant.biomass_used[1] / cofireplant.straw_supply.average_straw_yield


def total_income_benefit(cofireplant):
    """ Total benefit for the farmers from having extra income selling
        rice straw to the plant for co-firing
    """
    return farmer_income(cofireplant) * cultivation_area(cofireplant)
