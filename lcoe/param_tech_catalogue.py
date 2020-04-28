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
from pandas import read_excel

from model.utils import array, USD, MJ, kg, GJ, t
from manuscript1.parameters import emission_factor

from lcoe.plants_new import create_plant_dict_new, create_REplant_dict_new
from lcoe.plants import create_plant_dict, create_REplant_dict

# %% Read data and input parameters


def read_tech_data(sheetname):
    """Read xlsx data sheet from Vietnam Technology Catalogue and return a pandas dataframe."""
    df = read_excel(
        "Data/data_sheets_for_vietnam_technology_catalogue_-_english.xlsx",
        sheet_name=sheetname,
        header=0,
        skiprows=4,
        nrows=38,
        usecols="B:I",
        names=[
            "Parameter",
            "2020",
            "2030",
            "2050",
            "Lower20",
            "Upper20",
            "Lower50",
            "Upper50",
        ],
    )
    return df


CoalSC_data = read_tech_data("1 Coal supercritical")
CoalUSC_data = read_tech_data("1 Coal ultra-supercrital")
SCGT_data = read_tech_data("2 SCGT")
CCGT_data = read_tech_data("2 CCGT")
PV_data = read_tech_data("4 Solar PV")
Wind_onshore_data = read_tech_data("5 Wind onshore")
Wind_offshore_data = read_tech_data("5 Wind offshore")

# Coal subcritical sheet has extra column
CoalSub_data = read_excel(
    "Data/data_sheets_for_vietnam_technology_catalogue_-_english.xlsx",
    sheet_name="1 Coal subcritical",
    header=0,
    skiprows=4,
    nrows=38,
    usecols="B, D:J",
    names=[
        "Parameter",
        "2020",
        "2030",
        "2050",
        "Lower20",
        "Upper20",
        "Lower50",
        "Upper50",
    ],
)

# %% Data cleanup

# Missing uncertainty on SCGT Efficiency
# Our assumption: no uncertainty
SCGT_data["Lower20"][3] = SCGT_data["2020"][3]
SCGT_data["Upper20"][3] = SCGT_data["2020"][3]
SCGT_data["Lower50"][3] = SCGT_data["2050"][3]
SCGT_data["Upper50"][3] = SCGT_data["2050"][3]


Fuel = namedtuple("Fuel", "name, heat_value")
coal_6b = Fuel(
    name="6b_coal", heat_value=19.43468 * MJ / kg
)  # numerical value also used in emission_factor
coal_upper = Fuel(name="coal_upper", heat_value=19.43468 * MJ / kg)
coal_lower = Fuel(name="coal_lower", heat_value=19.43468 * MJ / kg)
coal_IEA = Fuel(name="coal_IEA", heat_value=19.43468 * MJ / kg)
coal_IEA_upper = Fuel(name="coal_IEA_upper", heat_value=19.43468 * MJ / kg)
coal_IEA_lower = Fuel(name="coal_IEA_lower", heat_value=19.43468 * MJ / kg)

natural_gas = Fuel(
    name="natural_gas", heat_value=47.1 * MJ / kg
)  # www.engineeringtoolbox.com
gas_upper = Fuel(name="gas_upper", heat_value=47.1 * MJ / kg)
gas_lower = Fuel(name="gas_lower", heat_value=47.1 * MJ / kg)
gas_IEA = Fuel(name="gas_IEA", heat_value=47.1 * MJ / kg)
gas_IEA_upper = Fuel(name="gas_IEA_upper", heat_value=47.1 * MJ / kg)
gas_IEA_lower = Fuel(name="gas_IEA_lower", heat_value=47.1 * MJ / kg)


# %%

fuel_price_data = read_excel(
    "Data/Fuel prices_LCOE.xlsx",
    sheet_name="FuelPrices",
    header=0,
    usecols="A, K, L",
    index_col=0,
    names=["Year", "Avg_coal", "Avg_gas"],
)

# %%

# Duval, Alice, and Benjamin Vandenbusche. 2018. EDDE Master thesis "Projet de Modélisation :
# Diversifier le Secteur Électrique Vietnamien Par plus de Gaz Peut Il Réduire l’exposition
# Au Risque-Prix Des Combustibles Fossiles ?"
# see file Data/prices_international_past_EIA.ods

coal_price_IEA = 55.71 * USD / t  # historical coal price (IEA) 20 year average
coal_price_2std = 18.16 * USD / t  # 2 standard deviation of historical coal price (IEA)
gas_price_IEA = (
    natural_gas.heat_value * 4.08 * USD / GJ
)  # historical gas price (IEA) 20y average
gas_price_2std = (
    natural_gas.heat_value * 2.54 * USD / GJ
)  # 2std of historical gas price (IEA)

fuel_price = dict()

fuel_price["6b_coal"] = {
    "2020": (
        array(
            fuel_price_data.loc["2020":"2050", "Avg_coal"]
            * coal_6b.heat_value
            * USD
            / GJ
        )
    ),
    "Lower20": (
        array(
            fuel_price_data.loc["2020":"2050", "Avg_coal"]
            * coal_6b.heat_value
            * USD
            / GJ
        )
    ),
    "Upper20": (
        array(
            fuel_price_data.loc["2020":"2050", "Avg_coal"]
            * coal_6b.heat_value
            * USD
            / GJ
        )
    ),
    "2030": (coal_6b.heat_value * float(fuel_price_data["Avg_coal"][2030]) * USD / GJ),
    "2050": (coal_6b.heat_value * float(fuel_price_data["Avg_coal"][2050]) * USD / GJ),
    "Lower50": (
        coal_6b.heat_value * float(fuel_price_data["Avg_coal"][2050]) * USD / GJ
    ),
    "Upper50": (
        coal_6b.heat_value * float(fuel_price_data["Avg_coal"][2050]) * USD / GJ
    ),
}

fuel_price["coal_upper"] = {}
for key in fuel_price["6b_coal"]:
    fuel_price["coal_upper"][key] = fuel_price["6b_coal"][key] + coal_price_2std

fuel_price["coal_lower"] = {}
for key in fuel_price["6b_coal"]:
    fuel_price["coal_lower"][key] = fuel_price["6b_coal"][key] - coal_price_2std

fuel_price["coal_IEA"] = {
    "2020": coal_price_IEA,  # IEA historical data, 20y average
    "Lower20": coal_price_IEA,
    "Upper20": coal_price_IEA,
    "2030": coal_price_IEA,
    "2050": coal_price_IEA,
    "Lower50": coal_price_IEA,
    "Upper50": coal_price_IEA,
}

fuel_price["coal_IEA_upper"] = {}
for key in fuel_price["coal_IEA"]:
    fuel_price["coal_IEA_upper"][key] = fuel_price["coal_IEA"][key] + coal_price_2std

fuel_price["coal_IEA_lower"] = {}
for key in fuel_price["coal_IEA"]:
    fuel_price["coal_IEA_lower"][key] = fuel_price["coal_IEA"][key] - coal_price_2std

fuel_price["natural_gas"] = {
    "2020": (
        array(
            fuel_price_data.loc["2020":"2050", "Avg_gas"]
            * natural_gas.heat_value
            * USD
            / GJ
        )
    ),
    "Lower20": (
        array(
            fuel_price_data.loc["2020":"2050", "Avg_gas"]
            * natural_gas.heat_value
            * USD
            / GJ
        )
    ),
    "Upper20": (
        array(
            fuel_price_data.loc["2020":"2050", "Avg_gas"]
            * natural_gas.heat_value
            * USD
            / GJ
        )
    ),
    "2030": (
        natural_gas.heat_value * float(fuel_price_data["Avg_gas"][2030]) * USD / GJ
    ),
    "2050": (
        natural_gas.heat_value * float(fuel_price_data["Avg_gas"][2050]) * USD / GJ
    ),
    "Lower50": (
        natural_gas.heat_value * float(fuel_price_data["Avg_gas"][2050]) * USD / GJ
    ),
    "Upper50": (
        natural_gas.heat_value * float(fuel_price_data["Avg_gas"][2050]) * USD / GJ
    ),
}

fuel_price["gas_upper"] = {}
for key in fuel_price["natural_gas"]:
    fuel_price["gas_upper"][key] = fuel_price["natural_gas"][key] + gas_price_2std

fuel_price["gas_lower"] = {}
for key in fuel_price["natural_gas"]:
    fuel_price["gas_lower"][key] = fuel_price["natural_gas"][key] - gas_price_2std

fuel_price["gas_IEA"] = {
    "2020": gas_price_IEA,
    "Lower20": gas_price_IEA,
    "Upper20": gas_price_IEA,
    "2030": gas_price_IEA,
    "2050": gas_price_IEA,
    "Lower50": gas_price_IEA,
    "Upper50": gas_price_IEA,
}
fuel_price["gas_IEA_upper"] = {}
for key in fuel_price["gas_IEA"]:
    fuel_price["gas_IEA_upper"][key] = fuel_price["gas_IEA"][key] + gas_price_2std

fuel_price["gas_IEA_lower"] = {}
for key in fuel_price["gas_IEA"]:
    fuel_price["gas_IEA_lower"][key] = fuel_price["gas_IEA"][key] - gas_price_2std

# %%

# Expand table imported manuscript1.parameter.py

emission_factor["natural_gas"] = {
    "CO2": 0.0561 * kg / MJ * natural_gas.heat_value,  # IPCC 2006
    "SO2": 0.012 * kg / t,  # EPA 1995, using NG density at 0.8 kg/m3
    "NOx": 2 * kg / t,  # EPA 1995, using NG density at 0.8 kg/m3
    "PM10": 0.0001 * kg / MJ * natural_gas.heat_value,
}  # IIASA RAINS documentation

emission_factor["coal_upper"] = emission_factor["6b_coal"]
emission_factor["coal_lower"] = emission_factor["6b_coal"]
emission_factor["coal_IEA"] = emission_factor["6b_coal"]
emission_factor["coal_IEA_upper"] = emission_factor["6b_coal"]
emission_factor["coal_IEA_lower"] = emission_factor["6b_coal"]
emission_factor["gas_upper"] = emission_factor["natural_gas"]
emission_factor["gas_lower"] = emission_factor["natural_gas"]
emission_factor["gas_IEA"] = emission_factor["natural_gas"]
emission_factor["gas_IEA_upper"] = emission_factor["natural_gas"]
emission_factor["gas_IEA_lower"] = emission_factor["natural_gas"]
emission_factor["RE"] = {
    "CO2": 0 * kg / t,
    "SO2": 0 * kg / t,
    "NOx": 0 * kg / t,
    "PM10": 0 * kg / t,
}

# %% Instantiate plants

coal_list = [coal_6b, coal_upper, coal_lower, coal_IEA, coal_IEA_upper, coal_IEA_lower]
gas_list = [natural_gas, gas_upper, gas_lower, gas_IEA, gas_IEA_upper, gas_IEA_lower]

Coal_Subcritical = create_plant_dict(
    "coal subcritical", CoalSub_data, coal_list, fuel_price, emission_factor
)
Coal_Supercritical = create_plant_dict(
    "coal supercritical", CoalSC_data, coal_list, fuel_price, emission_factor
)
Coal_USC = create_plant_dict(
    "coal USC", CoalUSC_data, coal_list, fuel_price, emission_factor
)

SCGT = create_plant_dict("SCGT", SCGT_data, gas_list, fuel_price, emission_factor)
CCGT = create_plant_dict("CCGT", CCGT_data, gas_list, fuel_price, emission_factor)

Coal_Subcritical_new = create_plant_dict_new(
    "coal subcritical", CoalSub_data, coal_list, fuel_price, emission_factor
)
Coal_Supercritical_new = create_plant_dict_new(
    "coal supercritical", CoalSC_data, coal_list, fuel_price, emission_factor
)
Coal_USC_new = create_plant_dict_new(
    "coal USC", CoalUSC_data, coal_list, fuel_price, emission_factor
)
SCGT_new = create_plant_dict_new(
    "SCGT", SCGT_data, gas_list, fuel_price, emission_factor
)
CCGT_new = create_plant_dict_new(
    "CCGT", CCGT_data, gas_list, fuel_price, emission_factor
)

assert Coal_Subcritical == Coal_Subcritical_new
assert Coal_Supercritical == Coal_Supercritical_new
assert Coal_USC == Coal_USC_new
assert SCGT == SCGT_new
assert CCGT == CCGT_new


Solar_PV = create_REplant_dict("solar", PV_data, fuel_price, emission_factor)
Wind_Onshore = create_REplant_dict(
    "onshore wind", Wind_onshore_data, fuel_price, emission_factor
)
Wind_Offshore = create_REplant_dict(
    "offshore wind", Wind_offshore_data, fuel_price, emission_factor
)

Solar_PV_new = create_REplant_dict_new("solar", PV_data, emission_factor)
Wind_Onshore_new = create_REplant_dict_new(
    "onshore wind", Wind_onshore_data, emission_factor
)
Wind_Offshore_new = create_REplant_dict_new(
    "offshore wind", Wind_offshore_data, emission_factor
)

# for idx, row in Solar_PV.items():
#    test = Solar_PV[idx] == Solar_PV_new[idx]
#    print(idx, test)


def compare_plant(plant, otherplant):
    """Test regression."""
    sameLCOE = plant.lcoe(0.1, 0.1, 20) == otherplant.lcoe(0.1, 0.1, 20)
    return sameLCOE


def same(old, new):
    """Compare two dicts of plants."""
    for idx, plant in old.items():
        if not compare_plant(plant, new[idx]):
            return False
    return True


assert same(Solar_PV, Solar_PV_new)
assert same(Wind_Onshore, Wind_Onshore_new)
assert same(Wind_Offshore, Wind_Offshore_new)
