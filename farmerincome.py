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

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import winder_rental_cost, straw
from strawdata import df
from natu.numpy import mean
from init import time_step


def farmer_income(plant):
    """ Extra income per hecta of rice cultivation for farmer from selling rice
        straw for co-firing after deducting the cost for renting straw winder

    """
    return bm_sell_revenue(plant) - winder_rental_cost / time_step


def bm_sell_revenue(plant):
    """ Revenue per hecta of rice cultivation for farmer from selling rice straw

    """
    if plant == MongDuong1:
        average_straw_yield = mean([df.loc['Bac Giang', 'straw yield'],
                                    df.loc['Hai Duong', 'straw yield'],
                                    df.loc['Hai Phong', 'straw yield'],
                                    df.loc['Quang Ninh', 'straw yield']
                                    ])
        return average_straw_yield * straw.price
    if plant == NinhBinh:
        return df.loc['Ninh Binh', 'straw yield'] * straw.price


def cultivation_area(plant):
    """ Area of rice cultivation needed to supply enough straw for co-firing

    """
    if plant == MongDuong1:
        average_straw_yield = mean([df.loc['Bac Giang', 'straw yield'],
                                    df.loc['Hai Duong', 'straw yield'],
                                    df.loc['Hai Phong', 'straw yield'],
                                    df.loc['Quang Ninh', 'straw yield'],
                                    ])
        return MongDuong1Cofire.biomass_used[1] / average_straw_yield
    if plant == NinhBinh:
        return NinhBinhCofire.biomass_used[1] / df.loc['Ninh Binh', 'straw yield']


def total_income_benefit(plant):
    """ Total benefit for the farmers from having extra income selling
        rice straw to the plant for co-firing

    """
    return farmer_income(plant) * cultivation_area(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
