# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Evaluation of benefits of co-firing project to public health"""
"""Assuming if there is no co-firing then all the amount of straw required for
co-firing would be burned in the field.
"""

from parameters import ef_so2_biomass, ef_pm10_biomass
from parameters import ef_nox_biomass, health_damage_so2
from parameters import health_damage_pm10, health_damage_nox
from biomassrequired import biomass_required
from coalsaved import coal_saved
from strawburned import so2_emission_field_base, pm10_emission_field_base
from strawburned import straw_burned_infield, nox_emission_field_base


def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value


""" Estimation of pollutant emission of baseline case. Emission of baseline case
include emission from open straw burning in the field and emission from coal
in the plant
"""


def so2_emission_plant_base(plant):
    """SO2 emission from the plant without co-firing.

    >>> from parameters import *
    >>> print_with_unit(so2_emission_plant_base, MongDuong1, 't/y')
    560.78 t/y
    >>> print_with_unit(so2_emission_plant_base, NinhBinh, 't/y')
    4951.36 t/y
    """
    return plant.base_coal_consumption * plant.ef_so2_coal * (1 - plant.desulfur_efficiency)


def so2_emission_base(plant):
    """ SO2 emission of baseline case

    >>> from parameters import *
    >>> print_with_unit(so2_emission_base, MongDuong1, 't/y')
    891.195 t/y
    >>> print_with_unit(so2_emission_base, NinhBinh, 't/y')
    5026.03 t/y
    """
    return so2_emission_plant_base(plant) + so2_emission_field_base(plant)


def pm10_emission_plant_base(plant):
    """ PM10 emission from the plant without co-firing.

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_plant_base, MongDuong1, 't/y')
    474.631 t/y
    >>> print_with_unit(pm10_emission_plant_base, NinhBinh, 't/y')
    89.8995 t/y
    """
    return plant.base_coal_consumption * plant.ef_pm10_coal * (1 - plant.esp_efficiency)


def pm10_emission_base(plant):
    """ PM10 emission of the baseline case

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_base, MongDuong1, 't/y')
    17179 t/y
    >>> print_with_unit(pm10_emission_base, NinhBinh, 't/y')
    3864.67 t/y
    """
    return pm10_emission_plant_base (plant) + pm10_emission_field_base(plant)


def nox_emission_plant_base(plant):
    """ NOx emission from the plant without co-firing.

    >>> from parameters import *
    >>> print_with_unit(nox_emission_plant_base, MongDuong1, 't/y')
    48763.5 t/y
    >>> print_with_unit(nox_emission_plant_base, NinhBinh, 't/y')
    7749.95 t/y
    """
    return plant.base_coal_consumption * plant.ef_nox_coal


def nox_emission_base(plant):
    """ NOx emission of baseline case

    >>> from parameters import *
    >>> print_with_unit(nox_emission_base, MongDuong1, 't/y')
    52948.8 t/y
    >>> print_with_unit(nox_emission_base, NinhBinh, 't/y')
    8695.72 t/y
    """
    return nox_emission_plant_base(plant) + nox_emission_field_base(plant)


""" Estimation of pollutant emission of co-firing case
"""

def so2_emission_field_cofire(plant):
    """ SO2 emission from open straw burning in co-firing case

    >>> from parameters import *
    >>> print_with_unit(so2_emission_field_cofire, MongDuong1, 't/y')
    289.657 t/y
    >>> print_with_unit(so2_emission_field_cofire, NinhBinh, 't/y')
    67.4808 t/y
    """
    return (straw_burned_infield(plant) - biomass_required(plant))* ef_so2_biomass


def so2_emission_plant_cofire(plant):
    """ SO2 emission from coal and straw combustion in plant

    >>> from parameters import *
    >>> print_with_unit(so2_emission_plant_cofire, MongDuong1, 't/y')
    533.296 t/y
    >>> print_with_unit(so2_emission_plant_cofire, NinhBinh, 't/y')
    4709.29 t/y
    """
    so2_emit_bm = biomass_required(plant) * ef_so2_biomass * (1 - plant.desulfur_efficiency)
    so2_emit_coal = (plant.base_coal_consumption - coal_saved(plant)) * plant.ef_so2_coal * (1 - plant.desulfur_efficiency)
    return so2_emit_bm + so2_emit_coal


def so2_emission_cofire(plant):
    """ SO2 emission of co-firing case

    >>> from parameters import *
    >>> print_with_unit(so2_emission_cofire, MongDuong1, 't/y')
    822.953 t/y
    >>> print_with_unit(so2_emission_cofire, NinhBinh, 't/y')
    4776.77 t/y
    """
    return so2_emission_plant_cofire(plant) + so2_emission_field_cofire(plant)

def pm10_emission_field_cofire(plant):
    """ PM10 emission from open straw burning in co-firing case

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_field_cofire, MongDuong1, 't/y')
    14643.8 t/y
    >>> print_with_unit(pm10_emission_field_cofire, NinhBinh, 't/y')
    3411.53 t/y
    """
    return (straw_burned_infield(plant) - biomass_required(plant))* ef_pm10_biomass


def pm10_emission_plant_cofire(plant):
    """PM10 emission from coal and straw combustion in plant

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_plant_cofire, MongDuong1, 't/y')
    458.991 t/y
    >>> print_with_unit(pm10_emission_plant_cofire, NinhBinh, 't/y')
    88.2799 t/y
    """
    pm10_emit_bm = biomass_required(plant) * ef_pm10_biomass * (1 - plant.esp_efficiency)
    pm10_emit_coal = (plant.base_coal_consumption - coal_saved(plant)) * plant.ef_pm10_coal * (1 - plant.esp_efficiency)
    return  pm10_emit_bm + pm10_emit_coal


def pm10_emission_cofire(plant):
    """ PM10 emission of co-firing case

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_cofire, MongDuong1, 't/y')
    15102.8 t/y
    >>> print_with_unit(pm10_emission_cofire, NinhBinh, 't/y')
    3499.81 t/y
    """
    return pm10_emission_plant_cofire(plant) + pm10_emission_field_cofire (plant)

def nox_emission_field_cofire(plant):
    """NOx emission from open straw burning in co-firing case

    >>> from parameters import *
    >>> print_with_unit(nox_emission_field_cofire, MongDuong1, 't/y')
    3668.99 t/y
    >>> print_with_unit(nox_emission_field_cofire, NinhBinh, 't/y')
    854.757 t/y
    """
    return (straw_burned_infield(plant) - biomass_required(plant))* ef_nox_biomass

def nox_emission_plant_cofire(plant):
    """NOx emission from co-firing

    >>> from parameters import *
    >>> print_with_unit(nox_emission_plant_cofire, MongDuong1, 't/y')
    46826.1 t/y
    >>> print_with_unit(nox_emission_plant_cofire, NinhBinh, 't/y')
    7450.83 t/y
    """
    nox_emit_bm = biomass_required(plant) * ef_nox_biomass
    nox_emit_coal = (plant.base_coal_consumption - coal_saved(plant)) * plant.ef_nox_coal
    return nox_emit_bm + nox_emit_coal

def nox_emission_cofire(plant):
    """ NOx emission in co-firing case

    >>> from parameters import *
    >>> print_with_unit(nox_emission_cofire, MongDuong1, 't/y')
    50495 t/y
    >>> print_with_unit(nox_emission_cofire, NinhBinh, 't/y')
    8305.59 t/y
    """
    return nox_emission_field_cofire(plant) + nox_emission_plant_cofire(plant)

""" Pollutant emission reduction is baseline emission minus co-firing emission
"""


def so2_emission_reduction(plant):
    """ Amount of SO2 emission cut off by co-firing

    >>> from parameters import *
    >>> print_with_unit(so2_emission_reduction, MongDuong1, 't/y')
    68.2423 t/y
    >>> print_with_unit(so2_emission_reduction, NinhBinh, 't/y')
    249.251 t/y
    """
    return so2_emission_base(plant) - so2_emission_cofire(plant)


def pm10_emission_reduction(plant):
    """ Amount of PM10 emission cut off by co-firing

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_reduction, MongDuong1, 't/y')
    2076.2 t/y
    >>> print_with_unit(pm10_emission_reduction, NinhBinh, 't/y')
    364.86 t/y
    """
    return pm10_emission_base(plant) - pm10_emission_cofire(plant)


def nox_emission_reduction(plant):
    """ Amount of NOx emission cut off by co-firing

    >>> from parameters import *
    >>> print_with_unit(nox_emission_reduction, MongDuong1, 't/y')
    2453.71 t/y
    >>> print_with_unit(nox_emission_reduction, NinhBinh, 't/y')
    390.132 t/y
    """
    return nox_emission_base(plant) - nox_emission_cofire(plant)

""" Health benefit from pollutant emission reduction is estimated using
specific health damage factor of each pollutant
"""


def health_benefit_so2(plant):
    """ Health benefit (in USD/year) from SO2 reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_so2, MongDuong1, 'kUSD/y')
    257.069 kUSD/y
    >>> print_with_unit(health_benefit_so2, NinhBinh, 'kUSD/y')
    938.929 kUSD/y
    """
    return so2_emission_reduction(plant) * health_damage_so2


def health_benefit_pm10(plant):
    """ Health benefit from pm10 reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_pm10, MongDuong1, 'kUSD/y')
    12214.3 kUSD/y
    >>> print_with_unit(health_benefit_pm10, NinhBinh, 'kUSD/y')
    2146.47 kUSD/y
    """
    return pm10_emission_reduction(plant) * health_damage_pm10

def health_benefit_nox(plant):
    """ Health benefit from nox emission reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_nox, MongDuong1, 'kUSD/y')
    701.762 kUSD/y
    >>> print_with_unit(health_benefit_nox, NinhBinh, 'kUSD/y')
    111.578 kUSD/y
    """
    return nox_emission_reduction(plant) * health_damage_nox

def total_health_benefit(plant):
    """ Total health benefit from co-firing

    >>> from parameters import *
    >>> print_with_unit(total_health_benefit, MongDuong1, 'kUSD/y')
    13173.1 kUSD/y
    >>> print_with_unit(total_health_benefit, NinhBinh, 'kUSD/y')
    3196.98 kUSD/y
    """
    return health_benefit_so2(plant) + health_benefit_pm10(plant) + health_benefit_nox(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
