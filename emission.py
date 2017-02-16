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
from biomasscost import bm_transportation_activity


def emission_coal_combust_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal combustion
       when there is no co-firing

    """
    return plant.emissions_controls.ef_coal_combust * plant.coal_consumption * plant.coal_supply.heat_value


def emission_coal_transport_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal transportation
       in no co-firing case. transported distance is 2 times of coal transport
       distance because round trip is accounted

    """
    return plant.emissions_controls.ef_coal_transport * 2 * plant.coal_supply.transport_distance * plant.coal_consumption


def emission_coal_combust_cofire(plant):
    """ emission from coal combustion when co-fire

    """
    return plant.emissions_controls.ef_coal_combust * (plant.coal_consumption - coal_saved(plant)) * plant.coal_supply.heat_value


def emission_coal_transport_cofire(plant):
    """emission from coal transportation when co-fire

    """
    return plant.emissions_controls.ef_coal_transport * 2 * plant.coal_supply.transport_distance * (plant.coal_consumption - coal_saved(plant))


def emission_biomass_combust(plant):
    """return the emission from biomass combustion with co-firing

    """
    return plant.ef_biomass_combust * biomass_required(plant) * biomass_heat_value


# FIXME: use the level of transport activity (t km)
def emission_biomass_transport(plant):
    """return emission from transportation of straw, which is transportation
    activity (t.km) multiplied by emission factor of transportation

    """
    return plant.ef_biomass_transport * bm_transportation_activity(plant)


def total_emission_coal(plant):
    """emission from coal in base case. only account for the percentage of coal
       substituted by biomass

    """
    return emission_coal_combust_base(plant) + emission_coal_transport_base(plant)


def total_emission_cofire(plant):
    """sum of emission from biomass combustion and biomass transportation for
       co-firing case

    """
    return (emission_biomass_combust(plant) +
            emission_biomass_transport(plant) +
            emission_coal_combust_cofire(plant) +
            emission_coal_transport_cofire(plant)
            )


def emission_reduction(plant):
    """different between total emission from coal (base case) and total
       emission from biomass (co-firing case)

    """
    return total_emission_coal(plant) - total_emission_cofire(plant)


def emission_reduction_benefit(plant):
    """ return the monetary benefit from greenhouse gas emission reduction

    """
    return emission_reduction(plant) * carbon_price

if __name__ == "__main__":
    import doctest
    doctest.testmod()
