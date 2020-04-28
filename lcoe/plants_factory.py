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

from model.utils import after_invest, hr, y, MW, MWh, USD, MUSD
from model.powerplant import PowerPlant, PlantParameter
from lcoe.param_economics import discount_rate, electricity_price

# If these capacity factors numbers come from tech catalogue,
# move them back in the module and pass them as parameter

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


# pylint: disable=too-many-arguments, too-many-locals
def plant(name, tech_data, year, emission_factor, fuel=None, fuel_price=None):
    """Create a power plant parametrized with Vietnam Technology Catalogue data.

    The argument 'name' (string type) take the technology name from full_load_hour dictionary.
    The argument 'tech_data' is the dataframe describing the technlogy.
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
    result = PowerPlant(
        plant_parameter,
        time_horizon=30,
        emission_factor=emission_factor,
        amount_invested=capital_idc,
    )
    if fuel is not None:
        result.mainfuel_cost = (
            result.mainfuel_used * fuel_price[str(fuel.name)][str(year)]
        )
    result.revenue = after_invest(
        result.power_generation[1] * electricity_price, result.time_horizon
    )
    return result


def plants_factory(
    tech_name, tech_data, emission_factor, fuel_price=None, fuel_list=None
):
    """Return a table of plants in 2020, 2030 & 2050.

    The table is a 1 dimensional dictionary if called with 3 arguments,
    or a dict of dict if the last two arguments are specified.
    """
    plant_dict = dict()
    for year in ["2020", "2030", "2050", "Lower20", "Upper20", "Lower50", "Upper50"]:
        if fuel_list is None:
            plant_dict[year] = plant(tech_name, tech_data, year, emission_factor)
        else:
            plant_dict[year] = {
                fuel.name: plant(
                    tech_name, tech_data, year, emission_factor, fuel, fuel_price
                )
                for fuel in fuel_list
            }
    return plant_dict
