# Economic of co-firing in two power plants in Vietnam
#
#  Greenhouse gas emissions reduction assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Greenhouse gas emissions assessment of a co-firing project.
   Total emission include emission from fuel combustion and fuel transportation
"""


from parameters import biomass_heat_value, carbon_price
from biomassrequired import biomass_required
from coalsaved import coal_saved
from units import time_step


def emission_coal_combust_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal combustion
       when there is no co-firing

    """
    return plant.coal.ef_combust * plant.coal_consumption * plant.coal.heat_value


def emission_coal_transport_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal transportation
       in no co-firing case. transported distance is 2 times of coal transport
       distance because round trip is accounted

    """
    return plant.coal.ef_transport * 2 * plant.coal.transport_distance * plant.coal_consumption


def emission_coal_combust_cofire(plant):
    """ emission from coal combustion when co-fire

    """
    return plant.coal.ef_combust * (plant.coal_consumption - coal_saved(plant)) * plant.coal.heat_value


def emission_coal_transport_cofire(plant):
    """emission from coal transportation when co-fire

    """
    return plant.coal.ef_transport * 2 * plant.coal.transport_distance * (plant.coal_consumption - coal_saved(plant))


def emission_biomass_combust(plant):
    """return the emission from biomass combustion with co-firing

    """
    return plant.ef_biomass_combust * biomass_required(plant) * biomass_heat_value


def emission_biomass_transport(cofiringplant):
    mass = cofiringplant.biomass.ef_transport * cofiringplant.active_chain.transport_tkm() / time_step
    mass.display_unit = 't/y'
    return mass


def total_emission_coal(plant):
    """emission from coal in base case. only account for the percentage of coal
       substituted by biomass

    """
    return emission_coal_combust_base(plant) + emission_coal_transport_base(plant)


def total_emission_cofire(plant, cofiringplant):
    """sum of emission from biomass combustion and biomass transportation for
       co-firing case

    """
    return (emission_biomass_combust(plant) +
            emission_biomass_transport(cofiringplant) +
            emission_coal_combust_cofire(plant) +
            emission_coal_transport_cofire(plant)
            )


def emission_reduction(plant, cofiringplant):
    """different between total emission from coal (base case) and total
       emission from biomass (co-firing case)

    """
    return total_emission_coal(plant) - total_emission_cofire(plant, cofiringplant)


def emission_reduction_benefit(plant, cofiringplant):
    """ return the monetary benefit from greenhouse gas emission reduction

    """
    return emission_reduction(plant, cofiringplant) * carbon_price

if __name__ == "__main__":
    import doctest
    doctest.testmod()
