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
from units import time_step, v_after_invest


def biomass_ratio_mass(biomass_ratio, heat_value_coal, heat_value_bm):
    """ Return the biomass/coal ratio in term of mass
    """
    assert 0 <= biomass_ratio
    return biomass_ratio * (heat_value_coal/heat_value_bm)


def boiler_efficiency_loss(bm_ratio_mass):
    """Calculate the boiler efficiency loss when co-firing biomass based on
    equation from Tillman 2000 with biomass ratio on mass basis

    >>> boiler_efficiency_loss(0)
    0.0
    """
    assert 0 <= bm_ratio_mass
    loss = 0.0044 * bm_ratio_mass * bm_ratio_mass + 0.0055 * bm_ratio_mass
    return loss


def boiler_efficiency_bm(plant):
    """Return the boiler efficiency when co-firing

    """
    ratio = biomass_ratio_mass(biomass_ratio, plant.coal.heat_value, biomass_heat_value)
    return plant.boiler_efficiency - boiler_efficiency_loss(ratio)


#def boiler_efficiency_bm(boiler_efficiency, boiler_efficiency_loss):
#    """Return the boiler efficiency when co-firing
#
#    >>> boiler_efficiency_bm(0, 0)
#    0
#    >>> boiler_efficiency_bm(1, 0)
#    1
#    """
#    assert 0 <= boiler_efficiency_loss < boiler_efficiency < 1
#    return boiler_efficiency - boiler_efficiency_loss


def plant_efficency_bm(plant):
    """ Plant efficiency with biomass co-firing

    """
    return (plant.plant_efficiency / plant.boiler_efficiency) * boiler_efficiency_bm(plant)


def gross_heat_input(plant):
    """total amount of heat needed to generate the same amount of electricity as in base case
    Not a vector
    """
    return plant.power_generation[0] / plant_efficency_bm(plant)


def biomass_required(plant):
    """Mass of biomass for co-firing
    """
    return gross_heat_input(plant) * biomass_ratio / biomass_heat_value


if __name__ == "__main__":
    import doctest
    doctest.testmod()
