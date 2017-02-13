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


from parameters import biomass_ratio, biomass_heat_value, MongDuong1, NinhBinh
from units import time_step
from natu.numpy import mean
from strawdata import df


def boiler_efficiency_loss(biomass_ratio):
    """Calculate the boiler efficiency loss when co-firing biomass based on
    equation from De & Assadi 2009.

    """
    loss = 0.0044 * biomass_ratio * biomass_ratio + 0.0055
    return loss


def boiler_efficiency_bm(plant):
    """Return the boiler efficiency when co-firing

    """
    return plant.base_boiler_efficiency - boiler_efficiency_loss(biomass_ratio)


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

    """
    return (plant.base_plant_efficiency / plant.base_boiler_efficiency) * boiler_efficiency_bm(plant)


def gross_heat_input(plant):
    """total amount of heat needed to generate the same amount of electricity as in base case

    """
    return plant.power_generation / plant_efficency_bm(plant) / time_step


def biomass_required(plant):
    """Amount of biomass needed per year for co-firing

    """
    return gross_heat_input(plant) * biomass_ratio / biomass_heat_value




if __name__ == "__main__":
    import doctest
    doctest.testmod()
