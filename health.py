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

from parameters import biomass_ratio, ef_so2_biomass, ef_pm10_biomass
from parameters import ef_nox_biomass, health_damage_so2
from parameters import health_damage_pm10, health_damage_nox

def coal_burned(plant):
    """ amount of coal substituted by 5% biomass co-firing

    >>> from parameters import *
    >>> coal_burned(MongDuong1)
    <Quantity(0.1375, 'megametric_ton / year')>
    >>> coal_burned(NinhBinh)
    <Quantity(0.021, 'megametric_ton / year')>
    """
    return plant.base_coal_consumption * biomass_ratio

def so2_emission_base(plant):
    """ SO2 emission from the plant without co-firing.
    Only account for the project (5% co-firing)

    >>> from parameters import *
    >>> so2_emission_base(MongDuong1)
    <Quantity(0.028462500000000026, 'kilogram * megametric_ton / metric_ton / year')>
    >>> so2_emission_base(NinhBinh)
    <Quantity(0.24150000000000002, 'kilogram * megametric_ton / metric_ton / year')>
    """
    return coal_burned(plant) * plant.ef_so2_coal * (1 - plant.desulfur_efficiency)


def pm10_emission_base(plant):
    """ PM10 emission from the plant without co-firing.
    Only account for the project

    >>> from parameters import *
    >>> pm10_emission_base(MongDuong1)
    <Quantity(0.02409000000000002, 'kilogram * megametric_ton / metric_ton / year')>
    >>> pm10_emission_base(NinhBinh)
    <Quantity(0.004384800000000004, 'kilogram * megametric_ton / metric_ton / year')>
    """
    return coal_burned(plant) * plant.ef_pm10_coal * (1 - plant.esp_efficiency)


def nox_emission_base(plant):
    """ NOx emission from the plant without co-firing.
    Only account for the project

    >>> from parameters import *
    >>> nox_emission_base(MongDuong1)
    <Quantity(2.475, 'kilogram * megametric_ton / metric_ton / year')>
    >>> nox_emission_base(NinhBinh)
    <Quantity(0.378, 'kilogram * megametric_ton / metric_ton / year')>
    """
    return coal_burned(plant) * plant.ef_nox_coal


def so2_emission_cofiring(plant):
    """ SO2 emission from co-firing

    >>> from parameters import *
    >>> so2_emission_cofiring(MongDuong1)
    <Quantity(839.5075682064047, 'gram * metric_ton / kilogram / year')>
    >>> so2_emission_cofiring(NinhBinh)
    <Quantity(9605.161131295841, 'gram * metric_ton / kilogram / year')>
    """
    return plant.biomass_required * ef_so2_biomass * (1 - plant.desulfur_efficiency)


def pm10_emission_cofiring(plant):
    """PM10 emission from co-firing

    >>> from parameters import *
    >>> pm10_emission_cofiring(MongDuong1)
    <Quantity(9431.504778615163, 'gram * metric_ton / kilogram / year')>
    >>> pm10_emission_cofiring(NinhBinh)
    <Quantity(3884.7540575463217, 'gram * metric_ton / kilogram / year')>
    """
    return plant.biomass_required * ef_pm10_biomass * (1 - plant.esp_efficiency)


def nox_emission_cofiring(plant):
    """NOx emission from co-firing

    >>> from parameters import *
    >>> nox_emission_cofiring(MongDuong1)
    <Quantity(590764.5850341361, 'gram * metric_ton / kilogram / year')>
    >>> nox_emission_cofiring(NinhBinh)
    <Quantity(121665.37432974733, 'gram * metric_ton / kilogram / year')>
    """
    return plant.biomass_required * ef_nox_biomass


def so2_emission_reduction(plant):
    """ Amount of SO2 emission cut off by co-firing

    >>> from parameters import *
    >>> so2_emission_reduction(MongDuong1)
    <Quantity(0.02762299243179362, 'kilogram * megametric_ton / metric_ton / year')>
    >>> so2_emission_reduction(NinhBinh)
    <Quantity(0.23189483886870418, 'kilogram * megametric_ton / metric_ton / year')>
    """
    return so2_emission_base(plant) - so2_emission_cofiring(plant)


def pm10_emission_reduction(plant):
    """ Amount of PM10 emission cut off by co-firing

    >>> from parameters import *
    >>> pm10_emission_reduction(MongDuong1)
    <Quantity(0.014658495221384859, 'kilogram * megametric_ton / metric_ton / year')>
    >>> pm10_emission_reduction(NinhBinh)
    <Quantity(0.0005000459424536821, 'kilogram * megametric_ton / metric_ton / year')>
    """
    return pm10_emission_base(plant) - pm10_emission_cofiring(plant)


def nox_emission_reduction(plant):
    """ Amount of NOx emission cut off by co-firing

    >>> from parameters import *
    >>> nox_emission_reduction(MongDuong1)
    <Quantity(1.884235414965864, 'kilogram * megametric_ton / metric_ton / year')>
    >>> nox_emission_reduction(NinhBinh)
    <Quantity(0.25633462567025267, 'kilogram * megametric_ton / metric_ton / year')>
    """
    return nox_emission_base(plant) - nox_emission_cofiring(plant)

def health_benefit_so2(plant):
    """ Health benefit (in USD/year) from SO2 reduction by co-firing

    >>> from parameters import *
    >>> health_benefit_so2(MongDuong1)
    <Quantity(104.05581249056657, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    >>> health_benefit_so2(NinhBinh)
    <Quantity(873.5478580184086, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    """
    return so2_emission_reduction(plant) * health_damage_so2


def health_benefit_pm10(plant):
    """ Health benefit from pm10 reduction by co-firing

    >>> from parameters import *
    >>> health_benefit_pm10(MongDuong1)
    <Quantity(86.23592738740713, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    >>> health_benefit_pm10(NinhBinh)
    <Quantity(2.941770279455012, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    """
    return pm10_emission_reduction(plant) * health_damage_pm10

def health_benefit_nox(plant):
    """ Health benefit from nox emission reduction by co-firing

    >>> from parameters import *
    >>> health_benefit_nox(MongDuong1)
    <Quantity(538.891328680237, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    >>> health_benefit_nox(NinhBinh)
    <Quantity(73.31170294169226, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    """
    return nox_emission_reduction(plant) * health_damage_nox

def total_health_benefit(plant):
    """ Total health benefit from co-firing

    >>> from parameters import *
    >>> total_health_benefit(MongDuong1)
    <Quantity(729.1830685582107, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    >>> total_health_benefit(NinhBinh)
    <Quantity(949.8013312395559, 'USD * kilogram * megametric_ton / metric_ton ** 2 / year')>
    """
    return health_benefit_so2(plant) + health_benefit_pm10(plant) + health_benefit_nox(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
