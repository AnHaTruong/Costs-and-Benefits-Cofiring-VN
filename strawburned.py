# Economic of co-firing in two power plants in Vietnam
#
# Open field burning of rice straw assessment
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

"""Estimation of pullutant emission of open field burning of rice straw of
the provinces that supply straw to the plant"""

from natu.math import fsum
from natu.units import t, y
from parameters import residue_to_product_ratio_straw, straw_burn_rate
from parameters import ef_so2_biomass, ef_pm10_biomass, ef_nox_biomass
from parameters import MongDuong1, NinhBinh
from strawdata import df


def straw_production(plant):
    """Straw production is rice production multiplied by straw to rice ratio

    """
    if plant == MongDuong1:
        rice_production = fsum([df.loc['Bac Giang', 'rice production (ton)']*t/y,
                                df.loc['Hai Duong', 'rice production (ton)']*t/y,
                                df.loc['Hai Phong', 'rice production (ton)']*t/y,
                                df.loc['Quang Ninh', 'rice production (ton)']*t/y
                                ])
        return rice_production * residue_to_product_ratio_straw
    
    if plant == NinhBinh:
        return df.loc['Ninh Binh', 'rice production (ton)']*t/y * residue_to_product_ratio_straw


def straw_burned_infield(plant):
    """Amount of straw burned in the open field after harvesting

    """
    return straw_production(plant) * straw_burn_rate


def so2_emission_field_base(plant):
    """SO2 emission from burning straw in field at provincial level

    """
    return straw_burned_infield(plant) * ef_so2_biomass


def nox_emission_field_base(plant):
    """SO2 emission from burning straw in field at provincial level

    """
    return straw_burned_infield(plant) * ef_nox_biomass


def pm10_emission_field_base(plant):
    """SO2 emission from burning straw in field at provincial level

    """
    return straw_burned_infield(plant) * ef_pm10_biomass

if __name__ == "__main__":
    import doctest
    doctest.testmod()