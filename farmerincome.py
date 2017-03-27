# encoding: utf-8
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

def total_income_benefit(plant, cofiringplant):
    """ Total benefit for the farmers from having extra income selling
        rice straw to the plant for co-firing
        The "plant" argument not used by here to keep regular with other _benefit functions
    """
    return cofiringplant.straw_supply.farm_income(winder_rental_cost, straw.price)[1]
