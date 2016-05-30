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
   Emission reduction is calculated for the co-firing part of the plant only
   Total emission include emission from fuel combustion and fuel transportation
"""

from parameters import biomass_heat_value


def emission_coal_combust(plant):
    """return the greenhouse gas emission in tonCO2eq from coal combustion
       when there is no co-firing

    >>> from parameters import *
    >>> emission_coal_combust(MongDuong1)
    292848 t/y
    >>> emission_coal_combust(NinhBinh)
    60310.8 t/y
    """
    return plant.ef_coal_combust * plant.coal_saved * plant.coal_heat_value


def emission_coal_transport(plant):
    """return the greenhouse gas emission in tonCO2eq from coal transportation
       in no co-firing case. transported distance is 2 times of coal transport
       distance because round trip is accounted

    >>> from parameters import *
    >>> emission_coal_transport(MongDuong1)
    0 t/y
    >>> emission_coal_transport(NinhBinh)
    305.839 t/y
    """
    return plant.ef_coal_transport * 2 * plant.coal_transport_distance * plant.coal_saved


def emission_biomass_combust(plant):
    """return the emission from burning the biomass when do co-firing

    >>> from parameters import *
    >>> emission_biomass_combust(MongDuong1)
    260107 t/y
    >>> emission_biomass_combust(NinhBinh)
    53568 t/y
    """
    return plant.ef_biomass_combust * plant.biomass_required * biomass_heat_value


def emission_biomass_transport(plant):
    """return emission from transportation of the biomass required for
       co-firing to the plant. transported distance is 2 times of biomass
       collection radius because round trip is accounted

    >>> from parameters import *
    >>> emission_biomass_transport(MongDuong1)
    2272.93 t/y
    >>> emission_biomass_transport(NinhBinh)
    104.066 t/y
    """
    return plant.ef_biomass_transport * 2 * plant.collection_radius * plant.biomass_required


def total_emission_coal(plant):
    """emission from coal in base case. only account for the percentage of coal
       substituted by biomass

    >>> from parameters import *
    >>> total_emission_coal(MongDuong1)
    292848 t/y
    >>> total_emission_coal(NinhBinh)
    60616.6 t/y
    """
    return emission_coal_combust(plant) + emission_coal_transport(plant)


def total_emission_biomass(plant):
    """sum of emission from biomass combustion and biomass transportation for
       co-firing case

    >>> from parameters import *
    >>> total_emission_biomass(MongDuong1)
    262380 t/y
    >>> total_emission_biomass(NinhBinh)
    53672.1 t/y
    """
    return emission_biomass_combust(plant) + emission_biomass_transport(plant)


def emission_reduction(plant):
    """different between total emission from coal (base case) and total
       emission from biomass (co-firing case)

    >>> from parameters import *
    >>> emission_reduction(MongDuong1)
    30467.9 t/y
    >>> emission_reduction(NinhBinh)
    6944.6 t/y
    """
    return total_emission_coal(plant) - total_emission_biomass(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()