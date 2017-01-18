# Economic of co-firing in two power plants in Vietnam
#
# Biomass required for co-firing
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Calculation of the amount of biomass needed for co-firing
    This calculation assumed that
    plant efficiency = boiler efficiency * efficiency of the rest of energy conversion chain
    (turbine, generator...)
"""


from parameters import biomass_ratio, biomass_heat_value
from unitsdef import time_step
#from classdef import MongDuong1, NinhBinh


def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value

def boiler_efficiency_loss(plant):
    """Calculate the boiler efficiency loss when co-firing biomass based on
    equation from De & Assadi 2009.

    >>> from parameters import *
    >>> boiler_efficiency_loss(MongDuong1)
    0.005510999999999999
    >>> boiler_efficiency_loss(NinhBinh)
    0.005510999999999999
    """
    loss = 0.0044 * biomass_ratio * biomass_ratio + 0.0055
    return loss


def boiler_efficiency_bm(plant):
    """Return the boiler efficiency when co-firing

    >>> from parameters import *
    >>> boiler_efficiency_bm(MongDuong1)
    0.8647889999999999
    >>> boiler_efficiency_bm(NinhBinh)
    0.810589
    """
    return plant.base_boiler_efficiency - boiler_efficiency_loss(plant)


#def boiler_efficiency_bm(boiler_efficiency, boiler_efficiency_loss):
#    """Return the boiler efficiency when co-firing
#
#    >>> boiler_efficiency_bm(0, 0)
#    0
#    >>> boiler_efficiency_bm(1, 0)
#    1
#    """<=
#    assert 0 <= boiler_efficiency_loss < base_boiler_efficiency < 1
#    return base_boiler_efficiency - boiler_efficiency_loss


def plant_efficency_bm(plant):
    """ Plant efficiency with biomass co-firing

    >>> from parameters import *
    >>> plant_efficency_bm(MongDuong1)
    0.3859405349879352
    >>> plant_efficency_bm(NinhBinh)
    0.21622990479107954
    """
    return (plant.base_plant_efficiency / plant.base_boiler_efficiency) * boiler_efficiency_bm(plant)


def gross_heat_input(plant):
    """total amount of heat needed to generate the same amount of electricity as in base case

    >>> from parameters import *
    >>> print_with_unit(gross_heat_input, MongDuong1, 'TJ/y')
    52985.7 TJ/y
    >>> print_with_unit(gross_heat_input, NinhBinh, 'TJ/y')
    9340.46 TJ/y
    """
    return plant.power_generation / plant_efficency_bm(plant) / time_step


def biomass_required(plant):
    """Amount of biomass needed per year for co-firing

    >>> from parameters import *
    >>> print_with_unit(biomass_required, MongDuong1, 't/y')
    226435 t/y
    >>> print_with_unit(biomass_required, NinhBinh, 't/y')
    39916.5 t/y
    """
    return gross_heat_input(plant) * biomass_ratio / biomass_heat_value

def cultivation_area(plant):
    """ Area of rice cultivation needed to supply enough straw for co-firing
    >>> print_with_unit(cultivation_area, MongDuong1, 'ha')
    40398.7 ha
    >>> print_with_unit(cultivation_area, NinhBinh, 'ha')
    7002.89 ha
    """
    return biomass_required(plant) / plant.biomass_yield

if __name__ == "__main__":
    import doctest
    doctest.testmod()
