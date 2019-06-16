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
import pandas as pd
import numpy as np
# pylint: disable=wrong-import-order
from model.utils import USD, after_invest
from model.powerplant import PowerPlant
from natu.units import MJ, kg, hr, MW, y, MUSD, MWh, GJ, t, kWh
from parameters import emission_factor, PlantParameter
discount_rate = 0.1
electricity_price = 0.08 * USD / kWh
tax_rate = 0.0

# %% Read data and input parameters


def read_tech_data(sheetname):
    """Read xlsx data sheet from Vietnam Technology Catalogue and return a pandas dataframe."""
    df = pd.read_excel("Data/data_sheets_for_vietnam_technology_catalogue_-_english.xlsx",
                       sheet_name=sheetname,
                       header=0, skiprows=4, nrows=38, usecols='B:I',
                       names=['Parameter', '2020', '2030', '2050', 'Lower20', 'Upper20',
                              'Lower50', 'Upper50'])
    return df


CoalSC_data = read_tech_data('1 Coal supercritical')
CoalUSC_data = read_tech_data('1 Coal ultra-supercrital')
SCGT_data = read_tech_data('2 SCGT')
CCGT_data = read_tech_data('2 CCGT')
PV_data = read_tech_data('4 Solar PV')
Wind_onshore_data = read_tech_data('5 Wind onshore')
Wind_offshore_data = read_tech_data('5 Wind offshore')

# Coal subcritical sheet has extra column
CoalSub_data = pd.read_excel("Data/data_sheets_for_vietnam_technology_catalogue_-_english.xlsx",
                             sheet_name='1 Coal subcritical',
                             header=0, skiprows=4, nrows=38, usecols='B, D:J',
                             names=['Parameter', '2020', '2030', '2050', 'Lower20', 'Upper20',
                                    'Lower50', 'Upper50'])
full_load_hour = {'coal subcritical': 6000 * hr,
                  'coal supercritical': 6000 * hr,
                  'coal USC': 6000 * hr,
                  'SCGT': 4000 * hr,
                  'CCGT': 4000 * hr,
                  'solar': 1800 * hr,
                  'onshore wind': 3600 * hr,
                  'offshore wind': 5200 * hr}

Fuel = namedtuple('Fuel', 'name, heat_value')
coal_6b = Fuel(name="6b_coal",
               heat_value=19.43468 * MJ / kg)  # numerical value also used in emission_factor
coal_upper = Fuel(name="coal_upper",
                  heat_value=19.43468 * MJ / kg)
coal_lower = Fuel(name="coal_lower",
                  heat_value=19.43468 * MJ / kg)

natural_gas = Fuel(name='natural_gas',
                   heat_value=47.1 * MJ / kg)  # www.engineeringtoolbox.com
gas_upper = Fuel(name='gas_upper',
                 heat_value=47.1 * MJ / kg)
gas_lower = Fuel(name='gas_lower',
                 heat_value=47.1 * MJ / kg)


# %%

fuel_price_data = pd.read_csv("Data/Fuel prices_LCOE.csv",
                              sep="\t", decimal=",",
                              header=0,
                              usecols=[0, 10, 11],
                              index_col=0,
                              names=['Year', 'Avg_coal', 'Avg_gas'])


# %%
#
#fuel_price_data = pd.read_excel("Data/Fuel prices_LCOE.xlsx",
#                                sheet_name='FuelPrices',
#                                header=0, usecols='A, K, L', index_col=0,
#                                names=['Year', 'Avg_coal', 'Avg_gas'])
# %%

coal_price_2std = 18.16 * USD / t  # 2 standard deviation of historical coal price (IEA)
gas_price_2std = natural_gas.heat_value * 2.69 * USD / GJ  # 2std of historical gas price (IEA)

fuel_price = dict()

fuel_price['6b_coal'] = {'2020': (np.array(fuel_price_data.loc['2020':'2050', 'Avg_coal'] *
                                  coal_6b.heat_value * USD / GJ)),
                         'Lower20': (np.array(fuel_price_data.loc['2020':'2050', 'Avg_coal'] *
                                     coal_6b.heat_value * USD / GJ)),
                         'Upper20': (np.array(fuel_price_data.loc['2020':'2050', 'Avg_coal'] *
                                     coal_6b.heat_value * USD / GJ)),
                         '2030': (coal_6b.heat_value *
                                  float(fuel_price_data['Avg_coal'][2030]) * USD / GJ),
                         '2050': (coal_6b.heat_value *
                                  float(fuel_price_data['Avg_coal'][2050]) * USD / GJ),
                         'Lower50': (coal_6b.heat_value *
                                     float(fuel_price_data['Avg_coal'][2050]) * USD / GJ),
                         'Upper50': (coal_6b.heat_value *
                                     float(fuel_price_data['Avg_coal'][2050]) * USD / GJ)}

fuel_price['coal_upper'] = {'2020': fuel_price['6b_coal']['2020'] + coal_price_2std,
                            'Lower20': fuel_price['6b_coal']['2020'] + coal_price_2std,
                            'Upper20': fuel_price['6b_coal']['2020'] + coal_price_2std,
                            '2030': fuel_price['6b_coal']['2030'] + coal_price_2std,
                            '2050': fuel_price['6b_coal']['2050'] + coal_price_2std,
                            'Lower50': fuel_price['6b_coal']['2050'] + coal_price_2std,
                            'Upper50': fuel_price['6b_coal']['2050'] + coal_price_2std}

fuel_price['coal_lower'] = {'2020': fuel_price['6b_coal']['2020'] - coal_price_2std,
                            'Lower20': fuel_price['6b_coal']['2020'] - coal_price_2std,
                            'Upper20': fuel_price['6b_coal']['2020'] - coal_price_2std,
                            '2030': fuel_price['6b_coal']['2030'] - coal_price_2std,
                            '2050': fuel_price['6b_coal']['2050'] - coal_price_2std,
                            'Lower50': fuel_price['6b_coal']['2050'] - coal_price_2std,
                            'Upper50': fuel_price['6b_coal']['2050'] - coal_price_2std}

fuel_price['natural_gas'] = {'2020': (np.array(fuel_price_data.loc['2020':'2050', 'Avg_gas'] *
                                      natural_gas.heat_value * USD / GJ)),
                             'Lower20': (np.array(fuel_price_data.loc['2020':'2050', 'Avg_gas'] *
                                         natural_gas.heat_value * USD / GJ)),
                             'Upper20': (np.array(fuel_price_data.loc['2020':'2050', 'Avg_gas'] *
                                         natural_gas.heat_value * USD / GJ)),
                             '2030': (natural_gas.heat_value *
                                      float(fuel_price_data['Avg_gas'][2030]) * USD / GJ),
                             '2050': (natural_gas.heat_value *
                                      float(fuel_price_data['Avg_gas'][2050]) * USD / GJ),
                             'Lower50': (natural_gas.heat_value *
                                         float(fuel_price_data['Avg_gas'][2050]) * USD / GJ),
                             'Upper50': (natural_gas.heat_value *
                                         float(fuel_price_data['Avg_gas'][2050]) * USD / GJ)}

fuel_price['gas_upper'] = {'2020': fuel_price['natural_gas']['2020'] + gas_price_2std,
                           'Lower20': fuel_price['natural_gas']['2020'] + gas_price_2std,
                           'Upper20': fuel_price['natural_gas']['2020'] + gas_price_2std,
                           '2030': fuel_price['natural_gas']['2030'] + gas_price_2std,
                           '2050': fuel_price['natural_gas']['2050'] + gas_price_2std,
                           'Lower50': fuel_price['natural_gas']['2050'] + gas_price_2std,
                           'Upper50': fuel_price['natural_gas']['2050'] + gas_price_2std}

fuel_price['gas_lower'] = {'2020': fuel_price['natural_gas']['2020'] - gas_price_2std,
                           'Lower20': fuel_price['natural_gas']['2020'] - gas_price_2std,
                           'Upper20': fuel_price['natural_gas']['2020'] - gas_price_2std,
                           '2030': fuel_price['natural_gas']['2030'] - gas_price_2std,
                           '2050': fuel_price['natural_gas']['2050'] - gas_price_2std,
                           'Lower50': fuel_price['natural_gas']['2050'] - gas_price_2std,
                           'Upper50': fuel_price['natural_gas']['2050'] - gas_price_2std}

emission_factor['natural_gas'] = {
    'CO2': 0.0561 * kg / MJ * natural_gas.heat_value,  # IPCC 2006
    'SO2': 0.012 * kg / t,  # EPA 1995, using NG density at 0.8 kg/m3
    'NOx': 2 * kg / t,  # EPA 1995, using NG density at 0.8 kg/m3
    'PM10': 0.0001 * kg / MJ * natural_gas.heat_value}  # IIASA RAINS documentation

emission_factor['coal_upper'] = emission_factor['6b_coal']
emission_factor['coal_lower'] = emission_factor['6b_coal']
emission_factor['gas_upper'] = emission_factor['natural_gas']
emission_factor['gas_lower'] = emission_factor['natural_gas']
emission_factor['RE'] = {
    'CO2': 0 * kg / t,
    'SO2': 0 * kg / t,
    'NOx': 0 * kg / t,
    'PM10': 0 * kg / t}
# %% Instantiate plants


def create_plant(name, tech_data, fuel, year):
    """Create a power plant with Vietnam Technology Catalogue data by PowerPlant class.

    The argument 'name' (string type) take the technology name from full_load_hour dictionary.
    The argument 'tech_data' is the pd dataframe of the technology.
    The argument 'fuel' is definded by Fuel.
    """
    plant_parameter = PlantParameter(name=name,
                                     capacity=tech_data[str(year)][1] * MW,
                                     capacity_factor=full_load_hour[name] / (8760 * hr),
                                     commissioning=2015,
                                     boiler_technology='CFB',
                                     boiler_efficiency_new=87.03 / 100,
                                     plant_efficiency=tech_data[str(year)][3] / 100,
                                     fix_om_coal=tech_data[str(year)][25] * USD / MW / y,
                                     variable_om_coal=tech_data[str(year)][26] * USD / MWh,
                                     emission_factor=emission_factor,
                                     emission_control={'CO2': 0.0,
                                                       'SO2': tech_data[year][19],
                                                       'NOx': 0.0, 'PM10': 0.996},
                                     coal=fuel,
                                     time_horizon=30)
    capital_cost = float(tech_data[str(year)][22]) * tech_data[str(year)][1] * MUSD
    construction_time = tech_data[str(year)][7]
    idc = (1 * ((1 + discount_rate) ** construction_time - 1) /
           (discount_rate * construction_time) * (1 + discount_rate / 2) - 1)
    capital_idc = capital_cost * (1 + idc)
    plant = PowerPlant(plant_parameter, capital=capital_idc)
    plant.coal_cost = plant.coal_used * fuel_price[str(fuel.name)][str(year)]
    plant.revenue = after_invest(plant.power_generation[1] * electricity_price,
                                 plant.parameter.time_horizon)
    return plant


coal_list = [coal_6b, coal_upper, coal_lower]
gas_list = [natural_gas, gas_upper, gas_lower]


def create_plant_dict(tech_name, tech_data, fuel_list):
    """Create a dictionary of convention plants in 2020, 2030 & 2050 with different fuel price."""
    plant_dict = dict()
    for year in ['2020', '2030', '2050', 'Lower20', 'Upper20', 'Lower50', 'Upper50']:
        plant_dict[year] = {}
        for fuel in fuel_list:
            arg = [tech_name, tech_data, fuel, year]
            plant = create_plant(*arg)
            plant_dict[year][fuel.name] = plant
    return plant_dict


Coal_Subcritical = create_plant_dict('coal subcritical', CoalSub_data, coal_list)
Coal_Supercritical = create_plant_dict('coal supercritical', CoalSC_data, coal_list)
Coal_USC = create_plant_dict('coal USC', CoalUSC_data, coal_list)

SCGT = create_plant_dict('SCGT', SCGT_data, gas_list)
CCGT = create_plant_dict('CCGT', CCGT_data, gas_list)


def create_RE_plant(name, tech_data, year):
    """Create a renewble power plant with Vietnam Technology Catalogue data by PowerPlant class.

    The argument 'name' (string type) take the technology name from full_load_hour dictionary.
    The argument 'tech_data' is the pd dataframe of the technlogy.
    """
    plant_parameter = PlantParameter(name=name,
                                     capacity=tech_data[str(year)][1] * MW,
                                     capacity_factor=full_load_hour[name] / (8760 * hr),
                                     commissioning=2015,
                                     boiler_technology='CFB',
                                     boiler_efficiency_new=87.03 / 100,
                                     plant_efficiency=1.0,
                                     fix_om_coal=tech_data[str(year)][25] * USD / MW / y,
                                     variable_om_coal=tech_data[str(year)][26] * USD / MWh,
                                     emission_factor=emission_factor,
                                     emission_control={'CO2': 0.0,
                                                       'SO2': 0.0,
                                                       'NOx': 0.0, 'PM10': 0.0},
                                     coal=coal_6b,
                                     time_horizon=30)
    capital_cost = float(tech_data[str(year)][22]) * tech_data[str(year)][1] * MUSD
    construction_time = tech_data[str(year)][7]
    idc = (1 * ((1 + discount_rate) ** construction_time - 1) /
           (discount_rate * construction_time) * (1 + discount_rate / 2) - 1)
    capital_idc = capital_cost * (1 + idc)
    plant = PowerPlant(plant_parameter, capital=capital_idc)
    plant.coal_used = np.ones(plant.parameter.time_horizon + 1) * 0.0 * t
    plant.coal_cost = plant.coal_used * fuel_price['6b_coal'][str(year)]
    plant.revenue = after_invest(plant.power_generation[1] * electricity_price,
                                 plant.parameter.time_horizon)
    return plant


def create_REplant_dict(tech_name, tech_data):
    """Create a dictionary of RE plants in 2020, 2030 and 2050."""
    plant_dict = dict()
    for year in ['2020', '2030', '2050', 'Lower20', 'Upper20', 'Lower50', 'Upper50']:
        arg = [tech_name, tech_data, year]
        plant = create_RE_plant(*arg)
        plant_dict[year] = plant
    return plant_dict


Solar_PV = create_REplant_dict('solar', PV_data)
Wind_Onshore = create_REplant_dict('onshore wind', Wind_onshore_data)
Wind_Offshore = create_REplant_dict('offshore wind', Wind_offshore_data)
