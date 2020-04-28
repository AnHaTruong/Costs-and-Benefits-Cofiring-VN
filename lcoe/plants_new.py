# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Instantiate technology data in Vietnam Technology Catalogue (Jakob Lundsager et al. 2019)
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Reproduce LCOE as calculated by DEA in EOR19 using parameter from VN Technology Catalogue."""

from model.utils import (
    USD,
    after_invest,
    hr,
    MW,
    y,
    MUSD,
    MWh,
)
from model.powerplant import PowerPlant, PlantParameter
from lcoe.param_economics import discount_rate, electricity_price

# If these capacity factors numbers come from tech catalogue,
# move them back in the module and import them

full_load_hour = {
    "coal subcritical": 6000 * hr,
    "coal supercritical": 6000 * hr,
    "coal USC": 6000 * hr,
    "SCGT": 4000 * hr,
    "CCGT": 4000 * hr,
    "solar": 1800 * hr,
    "onshore wind": 3600 * hr,
    "offshore wind": 5200 * hr,
}


# %% Instantiate plants

# pylint: disable=too-many-arguments, too-many-locals


def create_plant_new(
    name, tech_data, year, emission_factor, fuel=None, fuel_price=None
):
    """Create a renewble power plant with Vietnam Technology Catalogue data by PowerPlant class.

    The argument 'name' (string type) take the technology name from full_load_hour dictionary.
    The argument 'tech_data' is the pd dataframe of the technlogy.
    """
    if fuel is None:
        boiler_efficiency = None
        plant_efficiency = 1
        emission_control = None
    else:
        boiler_efficiency = 87.03 / 100
        plant_efficiency = tech_data[str(year)][3] / 100
        SO2control = tech_data[year][19]
        if SO2control == "-":
            SO2control = 0
        emission_control = {"CO2": 0.0, "SO2": SO2control, "NOx": 0.0, "PM10": 0.996}

    plant_parameter = PlantParameter(
        name=name,
        capacity=tech_data[str(year)][1] * MW,
        capacity_factor=full_load_hour[name] / (8760 * hr),
        commissioning=2015,
        boiler_technology="NA",
        boiler_efficiency_new=boiler_efficiency,
        plant_efficiency=plant_efficiency,
        fix_om_main=tech_data[str(year)][25] * USD / MW / y,
        variable_om_main=tech_data[str(year)][26] * USD / MWh,
        emission_control=emission_control,
        fuel=fuel,
    )
    capital_cost = float(tech_data[str(year)][22]) * tech_data[str(year)][1] * MUSD
    construction_time = tech_data[str(year)][7]
    idc = (
        1
        * ((1 + discount_rate) ** construction_time - 1)
        / (discount_rate * construction_time)
        * (1 + discount_rate / 2)
        - 1
    )
    capital_idc = capital_cost * (1 + idc)
    plant = PowerPlant(
        plant_parameter,
        time_horizon=30,
        emission_factor=emission_factor,
        amount_invested=capital_idc,
    )
    if plant_parameter.fuel is not None:
        plant.mainfuel_cost = (
            plant.mainfuel_used * fuel_price[str(fuel.name)][str(year)]
        )
    plant.revenue = after_invest(
        plant.power_generation[1] * electricity_price, plant.time_horizon
    )
    return plant


def create_plant_dict_new(tech_name, tech_data, emission_factor, fuel_price, fuel_list):
    """Create a dictionary of convention plants in 2020, 2030 & 2050 with different fuel price."""
    plant_dict = dict()
    for year in ["2020", "2030", "2050", "Lower20", "Upper20", "Lower50", "Upper50"]:
        plant_dict[year] = {}
        for fuel in fuel_list:
            arg = [tech_name, tech_data, year, emission_factor, fuel, fuel_price]
            plant = create_plant_new(*arg)
            plant_dict[year][fuel.name] = plant
    return plant_dict


def create_REplant_dict_new(tech_name, tech_data, emission_factor):
    """Create a dictionary of RE plants in 2020, 2030 and 2050."""
    plant_dict = dict()
    for year in ["2020", "2030", "2050", "Lower20", "Upper20", "Lower50", "Upper50"]:
        arg = [tech_name, tech_data, year, emission_factor]
        plant = create_plant_new(*arg)
        plant_dict[year] = plant
    return plant_dict
