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
from biomasscost import collection_radius, bm_transportation_activity
from units import print_with_unit


def emission_coal_combust_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal combustion
       when there is no co-firing

    >>> from parameters import *
    >>> print_with_unit(emission_coal_combust_base(MongDuong1), 't/y')
    5.08601e+06 t/y
    >>> print_with_unit(emission_coal_combust_base(NinhBinh), 't/y')
    896195 t/y
    """
    return plant.ef_coal_combust * plant.base_coal_consumption * plant.coal_heat_value


def emission_coal_transport_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal transportation
       in no co-firing case. transported distance is 2 times of coal transport
       distance because round trip is accounted

    >>> from parameters import *
    >>> print_with_unit(emission_coal_transport_base(MongDuong1), 't/y')
    0 t/y
    >>> print_with_unit(emission_coal_transport_base(NinhBinh), 't/y')
    12227.7 t/y
    """
    return plant.ef_coal_transport * 2 * plant.coal_transport_distance * plant.base_coal_consumption


def emission_coal_combust_cofire(plant):
    """ emission from coal combustion when co-fire

     >>> from parameters import *
    >>> print_with_unit(emission_coal_combust_cofire(MongDuong1), 't/y')
    4.83009e+06 t/y
    >>> print_with_unit(emission_coal_combust_cofire(NinhBinh), 't/y')
    851081 t/y
    """
    return plant.ef_coal_combust * (plant.base_coal_consumption - coal_saved(plant)) * plant.coal_heat_value


def emission_coal_transport_cofire(plant):
    """emission from coal transportation when co-fire

    >>> from parameters import *
    >>> print_with_unit(emission_coal_transport_cofire(MongDuong1), 't/y')
    0 t/y
    >>> print_with_unit(emission_coal_transport_cofire(NinhBinh), 't/y')
    11612.2 t/y
    """
    return plant.ef_coal_transport * 2 * plant.coal_transport_distance * (plant.base_coal_consumption - coal_saved(plant))


def emission_biomass_combust(plant):
    """return the emission from biomass combustion with co-firing

    >>> from parameters import *
    >>> print_with_unit(emission_biomass_combust(MongDuong1), 't/y')
    227309 t/y
    >>> print_with_unit(emission_biomass_combust(NinhBinh), 't/y')
    40070.6 t/y
    """
    return plant.ef_biomass_combust * biomass_required(plant) * biomass_heat_value

# FIXME: use the level of transport activity (t km)
def emission_biomass_transport(plant):
    """return emission from transportation of straw, which is transportation
    activity (t.km) multiplied by emission factor of transportation

    >>> from parameters import *
    >>> print_with_unit(emission_biomass_transport(MongDuong1), 't/y')
    3403.22 t/y
    >>> print_with_unit(emission_biomass_transport(NinhBinh), 't/y')
    119.635 t/y
    """
    return plant.ef_biomass_transport * bm_transportation_activity(plant)


def total_emission_coal(plant):
    """emission from coal in base case. only account for the percentage of coal
       substituted by biomass

    >>> from parameters import *
    >>> print_with_unit(total_emission_coal(MongDuong1), 't/y')
    5.08601e+06 t/y
    >>> print_with_unit(total_emission_coal(NinhBinh), 't/y')
    908423 t/y
    """
    return emission_coal_combust_base(plant) + emission_coal_transport_base(plant)


def total_emission_cofire(plant):
    """sum of emission from biomass combustion and biomass transportation for
       co-firing case

    >>> from parameters import *
    >>> print_with_unit(total_emission_cofire(MongDuong1), 't/y')
    5.0608e+06 t/y
    >>> print_with_unit(total_emission_cofire(NinhBinh), 't/y')
    902883 t/y
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
    >>> print_with_unit(emission_reduction(MongDuong1), 't/y')
    25209.1 t/y
    >>> print_with_unit(emission_reduction(NinhBinh), 't/y')
    5539.75 t/y
    """
    return total_emission_coal(plant) - total_emission_cofire(plant)


def emission_reduction_benefit(plant):
    """ return the monetary benefit from greenhouse gas emission reduction
    >>> from parameters import *
    >>> print_with_unit(emission_reduction_benefit(MongDuong1), 'USD/y')
    25209.1 USD/y
    >>> print_with_unit(emission_reduction_benefit(NinhBinh), 'USD/y')
    5539.75 USD/y
    """
    return emission_reduction(plant) * carbon_price

if __name__ == "__main__":
    import doctest
    doctest.testmod()
