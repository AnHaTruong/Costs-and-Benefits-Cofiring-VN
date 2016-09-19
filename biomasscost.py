# Economic of co-firing in two power plants in Vietnam
#
# Biomass cost
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Calculate the unit price of biomass for co-firing as delivered to the plant
    Unit price include fix price and transportation cost
"""

import math

from biomassrequired import biomass_required
from parameters import MongDuong1, transport_tariff, tortuosity_factor
from parameters import biomass_fix_cost, NinhBinh


def collection_area(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(collection_area, MongDuong1, 'km2')
    3934.22 km2
    >>> print_with_unit(collection_area, NinhBinh, 'km2')
    777.079 km2
    """
    if plant == MongDuong1:
        bm_supply_quangninh = math.pi * MongDuong1.small_radius ** 2 * MongDuong1.bm_density_1
        return (biomass_required(MongDuong1) - bm_supply_quangninh / 2)/MongDuong1.bm_density_2
    else:
        return biomass_required(NinhBinh) / NinhBinh.bm_density

def collection_radius(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(collection_radius, MongDuong1, 'km')
    70.7432 km
    >>> print_with_unit(collection_radius, NinhBinh, 'km')
    15.7274 km
    """
    if plant == MongDuong1:
        return ((2* collection_area(plant) / math.pi) + (MongDuong1.small_radius ** 2)) **0.5
    else:
        return (collection_area(plant) / math.pi) **0.5

def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value


def bm_transportation_cost(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(bm_transportation_cost, MongDuong1, 'USD/t')
    4.24459 USD/t
    >>> print_with_unit(bm_transportation_cost, NinhBinh, 'USD/t')
    0.943645 USD/t
    """
    return 2.0 / 3.0 * collection_radius(plant) * tortuosity_factor * transport_tariff 


def bm_unit_cost(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(bm_unit_cost, MongDuong1, 'USD/t')
    41.5046 USD/t
    >>> print_with_unit(bm_unit_cost, NinhBinh, 'USD/t')
    38.2036 USD/t
    """
    return bm_transportation_cost(plant) + biomass_fix_cost

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    