# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Define the model's input parameters.

All numeric values should be defined in this module,
except those defined in the parameters_supplychain module
"""

from collections import namedtuple

import pandas as pd

# pylint: disable=wrong-import-order
from init import USD, VND, ONES, after_invest
from natu.units import MJ, kg, t, d, hr, km, MW, ha, kW, y, kWh, MWh, g

from parameters_supplychain import supply_chain_MD1, supply_chain_NB
from system import System


discount_rate = 0.087771
depreciation_period = 10
tax_rate = 0.25               # Corporate tax in Vietnam
coal_import_price = 73 * USD / t

external_cost_SKC = pd.Series({'CO2': 1 * USD / t,
                               # Sakulniyomporn, Kubaha, and Chullabodhi (2011) RSER 15
                               'SO2': 3767 * USD / t,
                               'PM10': 5883 * USD / t,
                               'NOx': 286 * USD / t})

external_cost_ZWY = pd.Series({'CO2': 1 * USD / t,
                               # Zhang Q, Weili T, Yumei W, et al. (2007) Energy Policy 35
                               'SO2': 3680 * USD / t,
                               'PM10': 2625 * USD / t,
                               'NOx': 2438 * USD / t})

external_cost_HAS = pd.Series({'CO2': 1 * USD / t,
                               # Hainoun A, Almoustafa A, Seif Aldin M. (2010) Energy 35
                               'SO2': 1134 * USD / t,
                               'PM10': 2496 * USD / t,
                               'NOx': 1398 * USD / t})

external_cost = external_cost_SKC

mining_parameter = {'productivity_surface': 8.04 * t / hr,  # www.eia.g
                    'productivity_underground': 2.5 * t / hr,  # ww.eia.gov
                    'wage': 0 * USD / hr}

Fuel = namedtuple('Fuel', 'name, heat_value, transport_distance, transport_mean')

coal_6b = Fuel(name="6b_coal",
               heat_value=19.43468 * MJ / kg,  # numerical value also used in emission_factor
               transport_distance=0 * km,
               transport_mean='Conveyor belt')

coal_4b = Fuel(name="4b_coal",
               heat_value=21.5476 * MJ / kg,  # numerical value also used in emission_factor
               transport_distance=200 * km,
               transport_mean='Barge transport')

straw = Fuel(name='straw',
             heat_value=11.7 * MJ / kg,  # numerical value also used in emission_factor
             transport_distance='Endogenous',
             transport_mean='Road transport')

diesel_heat_value = 45.5 * MJ / kg   # ACEA

emission_factor = dict()

emission_factor['6b_coal'] = {
    'CO2': 0.0966 * kg / MJ * coal_6b.heat_value,  # IPCC 2006
    'SO2': 11.5 * kg / t,                          # Eastern Research Group (2011)
    'NOx': 18 * kg / t,                            # idem
    'PM10': 43.8 * kg / t}                         # idem

emission_factor['4b_coal'] = {
    'CO2': 0.0966 * kg / MJ * coal_4b.heat_value,  # IPCC 2006
    'SO2': emission_factor['6b_coal']['SO2'],
    'NOx': emission_factor['6b_coal']['NOx'],
    'PM10': 26.1 * kg / t}

emission_factor['diesel'] = {
    'CO2': 0.0705 * kg / MJ * diesel_heat_value,    # EPA AP-42, VolI, 3,3
    'SO2': 0.0004 * kg / MJ * diesel_heat_value,    # EPA AP-42, VolI, 3,3
    'NOx': 0.0018 * kg / MJ * diesel_heat_value,    # EPA AP-42, VolI, 3,3
    'PM10': 0.00014 * kg / MJ * diesel_heat_value}  # EPA AP-42, VolI, 3,3

emission_factor['Conveyor belt'] = {
    'CO2': 0 * kg / t / km,
    'SO2': 0 * kg / t / km,
    'NOx': 0 * kg / t / km,
    'PM10': 0 * kg / t / km}

emission_factor['road_transport'] = {
    'CO2': 0.110 * kg / t / km,          # Binh & Tuan (2016)
    'SO2': 0.003 * g / (20 * t) / km,    # http://naei.defra.gov.uk/data/ef-transport, year 2014
    'NOx': 2.68 * g / (20 * t) / km,     # idem
    'PM10': 0.04 * g / (20 * t) / km}    # idem

emission_factor['Barge transport'] = {
    'CO2': 0.071 * kg / t / km,                  # Binh & Tuan (2016)
    'SO2': 2 * g / kg * (8 * g / t / km),        # Van Dingenen et al. (2016)
    'NOx': 50.75 * g / kg * (8 * g / t / km),    # idem
    'PM10': 3.19 * g / kg * (8 * g / t / km)}    # idem

emission_factor['straw'] = {
    'CO2': 0.0858 * kg / MJ * 11.7 * MJ / kg,  # (Shafie & 2013)
    'SO2': 0.18 * kg / t,                      # (Hoang & 2013)
    'NOx': 2.28 * kg / t,                      # idem
    'PM10': 9.1 * kg / t}                      # idem

# hourly wage calculated from base salary defined in governmental regulations
farm_parameter = {'winder_rental_cost': 40 * USD / ha,   # per period
                  'winder_haul': 6.57 * t / d,
                  'work_hour_day': 8 * hr / d,
                  'wage_bm_collect': 1.11 * USD / hr,
                  'fuel_cost_per_hour': 0.5 * USD / hr,
                  'emission_factor': emission_factor,
                  'fuel_use': 4.16 * kg / d
                  }

transport_parameter = {'barge_fuel_consumption': 8 * g / t / km,  # Van Dingenen & 2016
                       'truck_loading_time': 2.7 / 60 * hr / t,  # Ovaskainen & Lundberg (2016)
                       'wage_bm_loading': 1.11 * USD / hr,
                       'truck_load': 20 * t,  # Also used in road_transport.emission_factor
                       'truck_velocity': 45 * km / hr,
                       'fuel_cost_per_hour_driving': 7.15 * USD / hr,
                       'fuel_cost_per_hour_loading': 0 * USD / hr,
                       'rental_cost_per_hour': 0 * USD / hr,
                       'wage_bm_transport': 1.11 * USD / hr,  # vantaiduongviet.com
                       'emission_factor': emission_factor}


PlantParameter = namedtuple("PlantParameter", ['name',
                                               'capacity',
                                               'capacity_factor',
                                               'commissioning',
                                               'boiler_technology',
                                               'boiler_efficiency',
                                               'plant_efficiency',
                                               'fix_om_coal',
                                               'variable_om_coal',
                                               'emission_factor',
                                               'emission_control',
                                               'coal'])

plant_parameter_MD1 = PlantParameter(name='Mong Duong 1',
                                     capacity=1080 * MW,
                                     capacity_factor=0.60,
                                     commissioning=2015,
                                     boiler_technology='CFB',
                                     boiler_efficiency=ONES * 87.03 / 100,
                                     plant_efficiency=ONES * 38.84 / 100,
                                     fix_om_coal=29.31 * USD / kW / y,
                                     variable_om_coal=0.0048 * USD / kWh,
                                     emission_factor=emission_factor,
                                     emission_control={'CO2': 0.0,
                                                       'SO2': 0.982, 'NOx': 0.0, 'PM10': 0.996},
                                     coal=coal_6b)


CofiringParameter = namedtuple('CofiringParameter', ['biomass_ratio_energy',
                                                     'capital_cost',
                                                     'fix_om_cost',
                                                     'variable_om_cost',
                                                     'biomass',
                                                     'boiler_efficiency_loss',
                                                     'OM_hour_MWh',
                                                     'wage_operation_maintenance'])


def boiler_efficiency_loss_quadratic(biomass_ratio_mass):
    """Boiler efficiency loss due to cofiring according to Tillman (2000)."""
    return 0.0044 * biomass_ratio_mass**2 + 0.0055 * biomass_ratio_mass


cofire_MD1 = CofiringParameter(biomass_ratio_energy=after_invest(0.05),
                               capital_cost=50 * USD / kW / y,
                               fix_om_cost=32.24 * USD / kW / y,
                               variable_om_cost=0.006 * USD / kWh,
                               biomass=straw,
                               boiler_efficiency_loss=boiler_efficiency_loss_quadratic,
                               OM_hour_MWh=0.12 * hr / MWh,  # working hour for OM per MWh
                               wage_operation_maintenance=1.67 * USD / hr)

Price = namedtuple('Price', 'biomass, transport, coal, electricity')

price_MD1 = Price(biomass=37.26 * USD / t,
                  transport=2000 * VND / t / km,
                  coal=1131400 * VND / t,
                  electricity=1239.17 * VND / kWh)

MongDuong1System = System(plant_parameter_MD1, cofire_MD1, supply_chain_MD1, price_MD1,
                          farm_parameter, transport_parameter)


plant_parameter_NB = PlantParameter(name='Ninh Binh',
                                    capacity=100 * MW,
                                    capacity_factor=0.64,
                                    commissioning=1974,
                                    boiler_technology='PC',
                                    boiler_efficiency=ONES * 81.61 / 100,
                                    plant_efficiency=ONES * 21.77 / 100,
                                    fix_om_coal=plant_parameter_MD1.fix_om_coal,
                                    variable_om_coal=plant_parameter_MD1.variable_om_coal,
                                    emission_factor=emission_factor,
                                    emission_control={'CO2': 0.0,
                                                      'SO2': 0.0, 'NOx': 0.0, 'PM10': 0.992},
                                    coal=coal_4b)


cofire_NB = cofire_MD1._replace(capital_cost=100 * USD / kW / y)

price_NB = price_MD1._replace(coal=1825730 * VND / t,   # Includes transport
                              electricity=1665.6 * VND / kWh)

NinhBinhSystem = System(plant_parameter_NB, cofire_NB, supply_chain_NB, price_NB,
                        farm_parameter, transport_parameter)
