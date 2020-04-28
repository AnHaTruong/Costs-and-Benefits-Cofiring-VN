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

from collections import namedtuple


from model.utils import (
    USD,
    after_invest,
    hr,
    kg,
    MJ,
    MW,
    y,
    MUSD,
    MWh,
    t,
)
from model.fuelpowerplant import FuelPowerPlant, PlantParameter
from lcoe.param_economics import discount_rate, electricity_price

# Unsure where these numbers come from

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

Fuel = namedtuple("Fuel", "name, heat_value")
coal_6b = Fuel(
    name="6b_coal", heat_value=19.43468 * MJ / kg
)  # numerical value also used in emission_factor


# %% Instantiate plants

# pylint: disable=too-many-arguments
def create_plant(name, tech_data, fuel, year, fuel_price, emission_factor):
    """Create a power plant with Vietnam Technology Catalogue data by PowerPlant class.

    The argument 'name' (string type) take the technology name from full_load_hour dictionary.
    The argument 'tech_data' is the pd dataframe of the technology.
    The argument 'fuel' is definded by Fuel.
    """
    SO2control = tech_data[year][19]
    if SO2control == "-":
        SO2control = 0
    plant_parameter = PlantParameter(
        name=name,
        capacity=tech_data[str(year)][1] * MW,
        capacity_factor=full_load_hour[name] / (8760 * hr),
        commissioning=2015,
        boiler_technology="CFB",
        boiler_efficiency_new=87.03 / 100,
        plant_efficiency=tech_data[str(year)][3] / 100,
        fix_om_fuel=tech_data[str(year)][25] * USD / MW / y,
        variable_om_fuel=tech_data[str(year)][26] * USD / MWh,
        emission_control={"CO2": 0.0, "SO2": SO2control, "NOx": 0.0, "PM10": 0.996},
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
    plant = FuelPowerPlant(
        plant_parameter,
        time_horizon=30,
        emission_factor=emission_factor,
        amount_invested=capital_idc,
    )
    plant.mainfuel_cost = plant.mainfuel_used * fuel_price[str(fuel.name)][str(year)]
    plant.revenue = after_invest(
        plant.power_generation[1] * electricity_price, plant.time_horizon
    )
    return plant


def create_plant_dict(tech_name, tech_data, fuel_list, fuel_price, emission_factor):
    """Create a dictionary of convention plants in 2020, 2030 & 2050 with different fuel price."""
    plant_dict = dict()
    for year in ["2020", "2030", "2050", "Lower20", "Upper20", "Lower50", "Upper50"]:
        plant_dict[year] = {}
        for fuel in fuel_list:
            arg = [tech_name, tech_data, fuel, year, fuel_price, emission_factor]
            plant = create_plant(*arg)
            plant_dict[year][fuel.name] = plant
    return plant_dict


def create_RE_plant(name, tech_data, year, fuel_price, emission_factor):
    """Create a renewble power plant with Vietnam Technology Catalogue data by PowerPlant class.

    The argument 'name' (string type) take the technology name from full_load_hour dictionary.
    The argument 'tech_data' is the pd dataframe of the technlogy.
    """
    plant_parameter = PlantParameter(
        name=name,
        capacity=tech_data[str(year)][1] * MW,
        capacity_factor=full_load_hour[name] / (8760 * hr),
        commissioning=2015,
        boiler_technology="CFB",
        boiler_efficiency_new=87.03 / 100,
        plant_efficiency=1.0,
        fix_om_fuel=tech_data[str(year)][25] * USD / MW / y,
        variable_om_fuel=tech_data[str(year)][26] * USD / MWh,
        emission_control={"CO2": 0.0, "SO2": 0.0, "NOx": 0.0, "PM10": 0.0},
        fuel=coal_6b,
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
    plant = FuelPowerPlant(
        plant_parameter,
        time_horizon=30,
        emission_factor=emission_factor,
        amount_invested=capital_idc,
    )
    plant.mainfuel_used = plant.ones * 0.0 * t
    plant.mainfuel_cost = plant.mainfuel_used * fuel_price["6b_coal"][str(year)]
    plant.revenue = after_invest(
        plant.power_generation[1] * electricity_price, plant.time_horizon
    )
    return plant


def create_REplant_dict(tech_name, tech_data, fuel_price, emission_factor):
    """Create a dictionary of RE plants in 2020, 2030 and 2050."""
    plant_dict = dict()
    for year in ["2020", "2030", "2050", "Lower20", "Upper20", "Lower50", "Upper50"]:
        arg = [tech_name, tech_data, year, fuel_price, emission_factor]
        plant = create_RE_plant(*arg)
        plant_dict[year] = plant
    return plant_dict
