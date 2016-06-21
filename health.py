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


def so2_emission_base(plant):
    """ SO2 emission from the plant without co-firing.
    Only account for the project (5% co-firing)

    >>> from parameters import *
    >>> so2_emission_base(MongDuong1)
    32.2893 t/y
    >>> so2_emission_base(NinhBinh)
    283.641 t/y
    """
    return plant.coal_saved * plant.ef_so2_coal * (1 - plant.desulfur_efficiency)


def pm10_emission_base(plant):
    """ PM10 emission from the plant without co-firing.
    Only account for the project

    >>> from parameters import *
    >>> pm10_emission_base(MongDuong1)
    27.3289 t/y
    >>> pm10_emission_base(NinhBinh)
    5.14993 t/y
    """
    return plant.coal_saved * plant.ef_pm10_coal * (1 - plant.esp_efficiency)


def nox_emission_base(plant):
    """ NOx emission from the plant without co-firing.
    Only account for the project

    >>> from parameters import *
    >>> nox_emission_base(MongDuong1)
    2807.76 t/y
    >>> nox_emission_base(NinhBinh)
    443.96 t/y
    """
    return plant.coal_saved * plant.ef_nox_coal


def so2_emission_cofiring(plant):
    """ SO2 emission from co-firing

    >>> from parameters import *
    >>> so2_emission_cofiring(MongDuong1)
    0.839508 t/y
    >>> so2_emission_cofiring(NinhBinh)
    9.60516 t/y
    """
    return plant.biomass_required * ef_so2_biomass * (1 - plant.desulfur_efficiency)


def pm10_emission_cofiring(plant):
    """PM10 emission from co-firing

    >>> from parameters import *
    >>> pm10_emission_cofiring(MongDuong1)
    9.4315 t/y
    >>> pm10_emission_cofiring(NinhBinh)
    3.88475 t/y
    """
    return plant.biomass_required * ef_pm10_biomass * (1 - plant.esp_efficiency)


def nox_emission_cofiring(plant):
    """NOx emission from co-firing

    >>> from parameters import *
    >>> pm10_emission_cofiring(MongDuong1)
    9.4315 t/y
    >>> pm10_emission_cofiring(NinhBinh)
    3.88475 t/y
    """
    return plant.biomass_required * ef_nox_biomass


def so2_emission_reduction(plant):
    """ Amount of SO2 emission cut off by co-firing

    >>> from parameters import *
    >>> so2_emission_reduction(MongDuong1)
    31.4498 t/y
    >>> so2_emission_reduction(NinhBinh)
    274.036 t/y
    """
    return so2_emission_base(plant) - so2_emission_cofiring(plant)


def pm10_emission_reduction(plant):
    """ Amount of PM10 emission cut off by co-firing

    >>> from parameters import *
    >>> pm10_emission_reduction(MongDuong1)
    17.8974 t/y
    >>> pm10_emission_reduction(NinhBinh)
    1.26518 t/y
    """
    return pm10_emission_base(plant) - pm10_emission_cofiring(plant)


def nox_emission_reduction(plant):
    """ Amount of NOx emission cut off by co-firing

    >>> from parameters import *
    >>> nox_emission_reduction(MongDuong1)
    2217 t/y
    >>> nox_emission_reduction(NinhBinh)
    322.294 t/y
    """
    return nox_emission_base(plant) - nox_emission_cofiring(plant)


def print_with_unit(func, plant, unit):
    l = func(plant)
    l.display_unit = unit
    return l
    

def health_benefit_so2(plant):
    """ Health benefit (in USD/year) from SO2 reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_so2, MongDuong1, 'kUSD/y')
    118.471 kUSD/y
    >>> print_with_unit(health_benefit_so2, NinhBinh, 'kUSD/y')
    1032.29 kUSD/y
    """
    return so2_emission_reduction(plant) * health_damage_so2


def health_benefit_pm10(plant):
    """ Health benefit from pm10 reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_pm10, MongDuong1, 'kUSD/y')
    105.29 kUSD/y
    >>> print_with_unit(health_benefit_pm10, NinhBinh, 'kUSD/y')
    7.44304 kUSD/y
    """
    return pm10_emission_reduction(plant) * health_damage_pm10

def health_benefit_nox(plant):
    """ Health benefit from nox emission reduction by co-firing

    >>> from parameters import *
    >>> print_with_unit(health_benefit_nox, MongDuong1, 'kUSD/y')
    634.062 kUSD/y
    >>> print_with_unit(health_benefit_nox, NinhBinh, 'kUSD/y')
    92.1762 kUSD/y
    """
    return nox_emission_reduction(plant) * health_damage_nox

def total_health_benefit(plant):
    """ Total health benefit from co-firing

    >>> from parameters import *
    >>> print_with_unit(total_health_benefit, MongDuong1, 'kUSD/y')
    857.823 kUSD/y
    >>> print_with_unit(total_health_benefit, NinhBinh, 'kUSD/y')
    1131.91 kUSD/y
    """
    return health_benefit_so2(plant) + health_benefit_pm10(plant) + health_benefit_nox(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
