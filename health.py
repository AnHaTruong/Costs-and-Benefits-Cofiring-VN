# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from parameters import emission_factor, specific_cost
from strawburned import straw_burned_infield

"""Evaluation of benefits of co-firing project to public health"""
"""Assuming if there is no co-firing then all the amount of straw required for
co-firing would be burned in the field.
"""

""" Estimation of pollutant emission of baseline case. Emission of baseline case
include emission from open straw burning in the field and emission from coal
in the plant
"""


def so2_emission_field_base(plant):
    """SO2 emission from burning straw in field at provincial level"""
    return straw_burned_infield(plant)[1] * emission_factor["Straw"]["SO2"]


def nox_emission_field_base(plant):
    """SO2 emission from burning straw in field at provincial level"""
    return straw_burned_infield(plant)[1] * emission_factor["Straw"]["NOx"]


def pm10_emission_field_base(plant):
    """SO2 emission from burning straw in field at provincial level"""
    return straw_burned_infield(plant)[1] * emission_factor["Straw"]["PM10"]


def so2_emission_plant_base(plant):
    """SO2 emission from the plant without co-firing."""
    return (plant.coal_used[1]
            * emission_factor[plant.coal.name]["SO2"]
            * (1 - plant.emission_controls["SO2"])
            )


def so2_emission_base(plant):
    """ SO2 emission of baseline case"""
    return so2_emission_plant_base(plant) + so2_emission_field_base(plant)


def pm10_emission_plant_base(plant):
    """ PM10 emission from the plant without co-firing."""
    return (plant.coal_used[1]
            * emission_factor[plant.coal.name]["PM10"]
            * (1 - plant.emission_controls["PM10"])
            )


def pm10_emission_base(plant):
    """ PM10 emission of the baseline case

    """
    return pm10_emission_plant_base(plant) + pm10_emission_field_base(plant)


def nox_emission_plant_base(plant):
    """ NOx emission from the plant without co-firing"""
    return plant.coal_used[1] * emission_factor[plant.coal.name]["NOx"]


def nox_emission_base(plant):
    """ NOx emission of baseline case"""
    return nox_emission_plant_base(plant) + nox_emission_field_base(plant)


""" Estimation of pollutant emission of co-firing case
"""


def so2_emission_field_cofire(plant, cofiringplant):
    """ SO2 emission from open straw burning in co-firing case"""
    return ((straw_burned_infield(plant)[1] - cofiringplant.biomass_used[1])
            * emission_factor["Straw"]["SO2"]
            )


def so2_emission_plant_cofire(plant, cofiringplant):
    """ SO2 emission from coal and straw combustion in plant"""
    so2_emit_bm = (cofiringplant.biomass_used[1]
                   * emission_factor["Straw"]["SO2"]
                   * (1 - plant.emission_controls["SO2"])
                   )
    so2_emit_coal = (cofiringplant.coal_used[1]
                     * emission_factor[plant.coal.name]["SO2"]
                     * (1 - plant.emission_controls["SO2"])
                     )
    return so2_emit_bm + so2_emit_coal


def so2_emission_cofire(plant, cofiringplant):
    """ SO2 emission of co-firing case"""
    return (so2_emission_plant_cofire(plant, cofiringplant)
            + so2_emission_field_cofire(plant, cofiringplant)
            )


def pm10_emission_field_cofire(plant, cofiringplant):
    """ PM10 emission from open straw burning in co-firing case
    """
    return ((straw_burned_infield(plant)[1] - cofiringplant.biomass_used[1])
            * emission_factor["Straw"]["PM10"]
            )


def pm10_emission_plant_cofire(plant, cofiringplant):
    """PM10 emission from coal and straw combustion in plant
    """
    pm10_emit_bm = (cofiringplant.biomass_used[1]
                    * emission_factor["Straw"]["PM10"]
                    * (1 - plant.emission_controls["PM10"])
                    )
    pm10_emit_coal = (cofiringplant.coal_used[1]
                      * emission_factor[plant.coal.name]["PM10"]
                      * (1 - plant.emission_controls["PM10"])
                      )
    return pm10_emit_bm + pm10_emit_coal


def pm10_emission_cofire(plant, cofiringplant):
    """ PM10 emission of co-firing case
    """
    return (pm10_emission_plant_cofire(plant, cofiringplant)
            + pm10_emission_field_cofire(plant, cofiringplant)
            )


def nox_emission_field_cofire(plant, cofiringplant):
    """NOx emission from open straw burning in co-firing case
    """
    return ((straw_burned_infield(plant)[1] - cofiringplant.biomass_used[1])
            * emission_factor["Straw"]["NOx"]
            )


def nox_emission_plant_cofire(plant, cofiringplant):
    """NOx emission from co-firing"""
    nox_emit_bm = cofiringplant.biomass_used[1] * emission_factor["Straw"]["NOx"]
    nox_emit_coal = cofiringplant.coal_used[1] * emission_factor[plant.coal.name]["NOx"]
    return nox_emit_bm + nox_emit_coal


def nox_emission_cofire(plant, cofiringplant):
    """ NOx emission in co-firing case"""
    return (nox_emission_field_cofire(plant, cofiringplant)
            + nox_emission_plant_cofire(plant, cofiringplant)
            )

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
    return so2_emission_reduction(plant, cofiringplant) * specific_cost['SO2']


def health_benefit_pm10(plant, cofiringplant):
    """ Health benefit from pm10 reduction by co-firing

    """
    return pm10_emission_reduction(plant, cofiringplant) * specific_cost['PM10']


def health_benefit_nox(plant, cofiringplant):
    """ Health benefit from nox emission reduction by co-firing

    """
    return nox_emission_reduction(plant, cofiringplant) * specific_cost['NOx']


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
