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


from parameters import biomass_heat_value, carbon_price
from biomassrequired import biomass_required
from coalsaved import coal_saved
from biomasscost import collection_radius


def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value


def emission_coal_combust_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal combustion
       when there is no co-firing

    >>> from parameters import *
    >>> emission_coal_combust_base(MongDuong1)
    5.16583e+06 t/y
    >>> emission_coal_combust_base(NinhBinh)
    874229 t/y
    """
    return plant.ef_coal_combust * plant.base_coal_consumption * plant.coal_heat_value


def emission_coal_transport_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal transportation
       in no co-firing case. transported distance is 2 times of coal transport
       distance because round trip is accounted

    >>> from parameters import *
    >>> emission_coal_transport_base(MongDuong1)
    0 t/y
    >>> emission_coal_transport_base(NinhBinh)
    11928 t/y
    """
    return plant.ef_coal_transport * 2 * plant.coal_transport_distance * plant.base_coal_consumption


def emission_coal_combust_cofire(plant):
    """ emission from coal combustion when co-fire
    """
    return plant.ef_coal_combust * (plant.base_coal_consumption - coal_saved(plant)) * plant.coal_heat_value


def emission_biomass_combust(plant):
    """return the emission from biomass combustion with co-firing

    >>> from parameters import *
    >>> print_with_unit(emission_biomass_combust, MongDuong1, 't/y')
    260107 t/y
    >>> print_with_unit(emission_biomass_combust, NinhBinh, 't/y')
    53568 t/y
    """
    return plant.ef_biomass_combust * biomass_required(plant) * biomass_heat_value


def emission_coal_transport_cofire(plant):
    """emission from coal transportation when co-fire
    """
    return plant.ef_coal_transport * 2 * plant.coal_transport_distance * (plant.base_coal_consumption - coal_saved(plant))

def emission_biomass_transport(plant):
    """return emission from transportation of biomass and coal.
       transported distance is 2 times of biomass
       collection radius because round trip is accounted

    >>> from parameters import *
    >>> print_with_unit(emission_biomass_transport, MongDuong1, 't/y')
    4032.62 t/y
    >>> print_with_unit(emission_biomass_transport, NinhBinh, 't/y')
    184.634 t/y
    """
    return plant.ef_biomass_transport * 2 * collection_radius(plant) * biomass_required(plant)


def total_emission_coal(plant):
    """emission from coal in base case. only account for the percentage of coal
       substituted by biomass

    >>> from parameters import *
    >>> print_with_unit(total_emission_coal, MongDuong1, 't/y')
    5.16583e+06 t/y
    >>> print_with_unit(total_emission_coal, NinhBinh, 't/y')
    886157 t/y
    """
    return emission_coal_combust_base(plant) + emission_coal_transport_base(plant)


def total_emission_cofire(plant):
    """sum of emission from biomass combustion and biomass transportation for
       co-firing case

    >>> from parameters import *
    >>> print_with_unit(total_emission_cofire, MongDuong1, 't/y')
    5.13712e+06 t/y
    >>> print_with_unit(total_emission_cofire, NinhBinh, 't/y')
    878776 t/y
    """
    return (emission_biomass_combust(plant)
            + emission_biomass_transport(plant)
            + emission_coal_combust_cofire(plant)
            + emission_coal_transport_cofire(plant)
           )

def emission_reduction(plant):
    """different between total emission from coal (base case) and total
       emission from biomass (co-firing case)

    >>> from parameters import *
    >>> emission_reduction(MongDuong1)
    28708.2 t/y
    >>> emission_reduction(NinhBinh)
    7381.07 t/y
    """
    return total_emission_coal(plant) - total_emission_cofire(plant)
    

def emission_reduction_benefit(plant):
    """ return the monetary benefit from greenhouse gas emission reduction
    >>> from parameters import *
    >>> print_with_unit(emission_reduction_benefit, MongDuong1, 'USD/y')
    28708.2 USD/y
    >>> print_with_unit(emission_reduction_benefit, NinhBinh, 'USD/y')
    7381.07 USD/y
    """
    return emission_reduction(plant) * carbon_price

if __name__ == "__main__":
    import doctest
    doctest.testmod()
