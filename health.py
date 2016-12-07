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

from parameters import ef_so2_biomass, ef_pm10_biomass
from parameters import ef_nox_biomass, health_damage_so2
from parameters import health_damage_pm10, health_damage_nox
from biomassrequired import biomass_required
from coalsaved import coal_saved


def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value


def so2_emission_base(plant):
    """ SO2 emission from the plant without co-firing.

    >>> from parameters import *
    >>> print_with_unit(so2_emission_base, MongDuong1, 't/y')
    569.581 t/y
    >>> print_with_unit(so2_emission_base, NinhBinh, 't/y')
    4830 t/y
    """
    return plant.base_coal_consumption * plant.ef_so2_coal * (1 - plant.desulfur_efficiency)


def pm10_emission_base(plant):
    """ PM10 emission from the plant without co-firing.
    Only account for the project

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_base, MongDuong1, 't/y')
    482.08 t/y
    >>> print_with_unit(pm10_emission_base, NinhBinh, 't/y')
    87.696 t/y
    """
    return plant.base_coal_consumption * plant.ef_pm10_coal * (1 - plant.esp_efficiency)


def nox_emission_base(plant):
    """ NOx emission from the plant without co-firing.
    Only account for the project

    >>> from parameters import *
    >>> print_with_unit(nox_emission_base, MongDuong1, 't/y')
    49528.8 t/y
    >>> print_with_unit(nox_emission_base, NinhBinh, 't/y')
    7560 t/y
    """
    return plant.base_coal_consumption * plant.ef_nox_coal


def so2_emission_cofiring(plant):
    """ SO2 emission from co-firing

    >>> from parameters import *
    >>> print_with_unit(so2_emission_cofiring, MongDuong1, 't/y')
    538.131 t/y
    >>> print_with_unit(so2_emission_cofiring, NinhBinh, 't/y')
    4506.4 t/y
    """
    so2_emit_bm = biomass_required(plant) * ef_so2_biomass * (1 - plant.desulfur_efficiency)
    so2_emit_coal = (plant.base_coal_consumption - coal_saved(plant)) * plant.ef_so2_coal * (1 - plant.desulfur_efficiency)
    return so2_emit_bm + so2_emit_coal


def pm10_emission_cofiring(plant):
    """PM10 emission from co-firing

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_cofiring, MongDuong1, 't/y')
    464.183 t/y
    >>> print_with_unit(pm10_emission_cofiring, NinhBinh, 't/y')
    85.5308 t/y
    """
    pm10_emit_bm = biomass_required(plant) * ef_pm10_biomass * (1 - plant.esp_efficiency)
    pm10_emit_coal = (plant.base_coal_consumption - coal_saved(plant)) * plant.ef_pm10_coal * (1 - plant.esp_efficiency)
    return  pm10_emit_bm + pm10_emit_coal


def nox_emission_cofiring(plant):
    """NOx emission from co-firing

    >>> from parameters import *
    >>> print_with_unit(nox_emission_cofiring, MongDuong1, 't/y')
    47311.8 t/y
    >>> print_with_unit(nox_emission_cofiring, NinhBinh, 't/y')
    7160.12 t/y
    """
    nox_emit_bm = biomass_required(plant) * ef_nox_biomass
    nox_emit_coal = (plant.base_coal_consumption - coal_saved(plant)) * plant.ef_nox_coal
    return nox_emit_bm + nox_emit_coal


def so2_emission_reduction(plant):
    """ Amount of SO2 emission cut off by co-firing

    >>> from parameters import *
    >>> print_with_unit(so2_emission_reduction, MongDuong1, 't/y')
    31.4498 t/y
    >>> print_with_unit(so2_emission_reduction, NinhBinh, 't/y')
    323.604 t/y
    """
    return so2_emission_base(plant) - so2_emission_cofiring(plant)


def pm10_emission_reduction(plant):
    """ Amount of PM10 emission cut off by co-firing

    >>> from parameters import *
    >>> print_with_unit(pm10_emission_reduction, MongDuong1, 't/y')
    17.8974 t/y
    >>> print_with_unit(pm10_emission_reduction, NinhBinh, 't/y')
    2.16517 t/y
    """
    return pm10_emission_base(plant) - pm10_emission_cofiring(plant)


def nox_emission_reduction(plant):
    """ Amount of NOx emission cut off by co-firing

    >>> from parameters import *
    >>> print_with_unit(nox_emission_reduction, MongDuong1, 't/y')
    2217 t/y
    >>> print_with_unit(nox_emission_reduction, NinhBinh, 't/y')
    399.879 t/y
    """
    return nox_emission_base(plant) - nox_emission_cofiring(plant)


def health_benefit_so2(plant):
    """ Health benefit (in USD/year) from SO2 reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_so2, MongDuong1, 'kUSD/y')
    118.471 kUSD/y
    >>> print_with_unit(health_benefit_so2, NinhBinh, 'kUSD/y')
    1219.02 kUSD/y
    """
    return so2_emission_reduction(plant) * health_damage_so2


def health_benefit_pm10(plant):
    """ Health benefit from pm10 reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_pm10, MongDuong1, 'kUSD/y')
    105.29 kUSD/y
    >>> print_with_unit(health_benefit_pm10, NinhBinh, 'kUSD/y')
    12.7377 kUSD/y
    """
    return pm10_emission_reduction(plant) * health_damage_pm10

def health_benefit_nox(plant):
    """ Health benefit from nox emission reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_nox, MongDuong1, 'kUSD/y')
    634.062 kUSD/y
    >>> print_with_unit(health_benefit_nox, NinhBinh, 'kUSD/y')
    114.366 kUSD/y
    """
    return nox_emission_reduction(plant) * health_damage_nox

def total_health_benefit(plant):
    """ Total health benefit from co-firing

    >>> from parameters import *
    >>> print_with_unit(total_health_benefit, MongDuong1, 'kUSD/y')
    857.823 kUSD/y
    >>> print_with_unit(total_health_benefit, NinhBinh, 'kUSD/y')
    1346.12 kUSD/y
    """
    return health_benefit_so2(plant) + health_benefit_pm10(plant) + health_benefit_nox(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
