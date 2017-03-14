# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from parameters import emission_factor
from parameters import health_damage_so2, health_damage_pm10, health_damage_nox
from strawburned import so2_emission_field_base, pm10_emission_field_base
from strawburned import straw_burned_infield, nox_emission_field_base

"""Evaluation of benefits of co-firing project to public health"""
"""Assuming if there is no co-firing then all the amount of straw required for
co-firing would be burned in the field.
"""

""" Estimation of pollutant emission of baseline case. Emission of baseline case
include emission from open straw burning in the field and emission from coal
in the plant
"""


def so2_emission_plant_base(plant):
    """SO2 emission from the plant without co-firing.

    """
    return plant.coal_used[1] * plant.coal.ef_so2 * (1 - plant.desulfur_efficiency)


def so2_emission_base(plant):
    """ SO2 emission of baseline case

    """
    return so2_emission_plant_base(plant) + so2_emission_field_base(plant)


def pm10_emission_plant_base(plant):
    """ PM10 emission from the plant without co-firing.

    """
    return plant.coal_used[1] * plant.coal.ef_pm10 * (1 - plant.esp_efficiency)


def pm10_emission_base(plant):
    """ PM10 emission of the baseline case

    """
    return pm10_emission_plant_base(plant) + pm10_emission_field_base(plant)


def nox_emission_plant_base(plant):
    """ NOx emission from the plant without co-firing.

    """
    return plant.coal_used[1] * plant.coal.ef_nox


def nox_emission_base(plant):
    """ NOx emission of baseline case

    """
    return nox_emission_plant_base(plant) + nox_emission_field_base(plant)


""" Estimation of pollutant emission of co-firing case
"""


def so2_emission_field_cofire(plant, cofiringplant):
    """ SO2 emission from open straw burning in co-firing case

    """
    return (straw_burned_infield(plant) - cofiringplant.biomass_used[1]) * emission_factor["Straw"]["SO2"]


def so2_emission_plant_cofire(plant, cofiringplant):
    """ SO2 emission from coal and straw combustion in plant

    """
    so2_emit_bm = cofiringplant.biomass_used[1] * emission_factor["Straw"]["SO2"] * (1 - plant.desulfur_efficiency)
    so2_emit_coal = (cofiringplant.coal_used[1] *
                     plant.coal.ef_so2 *
                     (1 - plant.desulfur_efficiency)
                     )
    return so2_emit_bm + so2_emit_coal


def so2_emission_cofire(plant, cofiringplant):
    """ SO2 emission of co-firing case

    """
    return so2_emission_plant_cofire(plant, cofiringplant) + so2_emission_field_cofire(plant, cofiringplant)


def pm10_emission_field_cofire(plant, cofiringplant):
    """ PM10 emission from open straw burning in co-firing case
    """
    return (straw_burned_infield(plant) - cofiringplant.biomass_used[1]) * emission_factor["Straw"]["PM10"]


def pm10_emission_plant_cofire(plant, cofiringplant):
    """PM10 emission from coal and straw combustion in plant
    """
    pm10_emit_bm = cofiringplant.biomass_used[1] * emission_factor["Straw"]["PM10"] * (1 - plant.esp_efficiency)
    pm10_emit_coal = (cofiringplant.coal_used[1]*
                      plant.coal.ef_pm10 *
                      (1 - plant.esp_efficiency)
                      )
    return pm10_emit_bm + pm10_emit_coal


def pm10_emission_cofire(plant, cofiringplant):
    """ PM10 emission of co-firing case
    """
    return pm10_emission_plant_cofire(plant, cofiringplant) + pm10_emission_field_cofire(plant, cofiringplant)


def nox_emission_field_cofire(plant, cofiringplant):
    """NOx emission from open straw burning in co-firing case
    """
    return (straw_burned_infield(plant) - cofiringplant.biomass_used[1]) * emission_factor["Straw"]["NOx"]



def nox_emission_plant_cofire(plant, cofiringplant):
    """NOx emission from co-firing

    """
    nox_emit_bm = cofiringplant.biomass_used[1] * emission_factor["Straw"]["NOx"]
    nox_emit_coal = cofiringplant.coal_used[1] * plant.coal.ef_nox
    return nox_emit_bm + nox_emit_coal


def nox_emission_cofire(plant, cofiringplant):
    """ NOx emission in co-firing case

    """
    return nox_emission_field_cofire(plant, cofiringplant) + nox_emission_plant_cofire(plant, cofiringplant)

""" Pollutant emission reduction is baseline emission minus co-firing emission
"""


def so2_emission_reduction(plant, cofiringplant):
    """ Amount of SO2 emission cut off by co-firing

    """
    return so2_emission_base(plant) - so2_emission_cofire(plant, cofiringplant)


def pm10_emission_reduction(plant, cofiringplant):
    """ Amount of PM10 emission cut off by co-firing

    """
    return pm10_emission_base(plant) - pm10_emission_cofire(plant, cofiringplant)


def nox_emission_reduction(plant, cofiringplant):
    """ Amount of NOx emission cut off by co-firing

    """
    return nox_emission_base(plant) - nox_emission_cofire(plant, cofiringplant)

""" Health benefit from pollutant emission reduction is estimated using
specific health damage factor of each pollutant
"""


def health_benefit_so2(plant, cofiringplant):
    """ Health benefit (in USD/year) from SO2 reduction by co-firing

    """
    return so2_emission_reduction(plant, cofiringplant) * health_damage_so2


def health_benefit_pm10(plant, cofiringplant):
    """ Health benefit from pm10 reduction by co-firing

    """
    return pm10_emission_reduction(plant, cofiringplant) * health_damage_pm10


def health_benefit_nox(plant, cofiringplant):
    """ Health benefit from nox emission reduction by co-firing

    """
    return nox_emission_reduction(plant, cofiringplant) * health_damage_nox


def total_health_benefit(plant, cofiringplant):
    """ Total health benefit from co-firing
    """
    return (health_benefit_so2(plant, cofiringplant) +
            health_benefit_pm10(plant, cofiringplant) +
            health_benefit_nox(plant, cofiringplant)
            )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
