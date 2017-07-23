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
"""Input parameters of the model

All numeric values should be defined in this module.
"""

from collections import namedtuple

import pandas as pd

from init import USD, VND, time_horizon, v_after_invest
from natu.units import MJ, kg, t, d, hr, km, MW, ha, kW, y, kWh, MWh, g
from natu.numpy import full

from strawdata import MongDuong1_straw_density1, MongDuong1_straw_density2
from strawdata import NinhBinh_straw_density, NinhBinh_straw_production
from strawdata import MongDuong1_straw_production
from strawdata import MongDuong1_average_straw_yield, NinhBinh_average_straw_yield

from PowerPlant import PowerPlant
from Shape import Semi_Annulus, Disk
from SupplyChain import SupplyChain, SupplyZone
from System import System

discount_rate = 0.087771
depreciation_period = 10
tax_rate = 0.25               # Corporate tax in Vietnam
feedin_tariff = {'MD': 1239.17 * VND / kWh,
                 'NB': 1665.6 * VND / kWh}

# hourly wage calculated from base salary defined in governmental regulations

collect_economics = {'winder_rental_cost': 40 * USD / ha,   # per period
                     'winder_haul': 6.57 * t / d,
                     'work_hour_day': 8 * hr / d,
                     'wage_bm_collect': 1.11 * USD / hr
                     }

truck_economics = {'truck_loading_time': 2.7 / 60 * hr / t,  # (Ovaskainen & 2016 )
                   'wage_bm_loading': 1.11 * USD / hr,
                   'truck_load': 20 * t,
                   'truck_velocity': 45 * km / hr,
                   'wage_bm_transport': 1.11 * USD / hr,
                   'transport_tariff': 2000 * VND / t / km}  # vantaiduongviet.com

barge_fuel_consumption = 8 * g / t / km  # Van Dingenen & 2016
mining_productivity_surface = 8.04 * t / hr  # www.eia.g
mining_productivity_underground = 2.5 * t / hr  # ww.eia.gov
coal_import_price = 73 * USD / t

Fuel = namedtuple('Fuel', 'name, heat_value, price, transport_distance, transport_mean')

MD_Coal = Fuel(name="6b_coal",
               heat_value=19.43468 * MJ / kg,
               price=1131400 * VND / t,
               transport_distance=0 * km,
               transport_mean='Conveyor belt'
               )

NB_Coal = Fuel(name="4b_coal",
               heat_value=21.5476 * MJ / kg,
               price=1825730 * VND / t,  # Includes transport
               transport_distance=200 * km,
               transport_mean='Barge transport'
               )

straw = Fuel(name='Straw',
             heat_value=11.7 * MJ / kg,
             price=37.26 * USD / t,
             transport_distance='Endogenous',
             transport_mean='Road transport'
             )

emission_factor = {
    '6b_coal': {'CO2': 0.0966 * kg / MJ * MD_Coal.heat_value,  # IPCC 2006
                # Eastern Research Group (2011)
                'SO2': 11.5 * kg / t,
                'NOx': 18 * kg / t,
                'PM10': 43.8 * kg / t
                },
    '4b_coal': {'CO2': 0.0966 * kg / MJ * NB_Coal.heat_value,  # IPCC 2006
                # Eastern Research Group (2011)
                'SO2': 11.5 * kg / t,
                'NOx': 18 * kg / t,
                'PM10': 26.1 * kg / t
                },
    'Straw': {'CO2': 0.0858 * kg / MJ * straw.heat_value,  # (Shafie & 2013)
              # (Hoang & 2013)
              'SO2': 0.18 * kg / t,
              'NOx': 2.28 * kg / t,
              'PM10': 9.1 * kg / t
              },
    'Conveyor belt': {'CO2': 0.0 * kg / t / km,
                      'SO2': 0. * kg / t / km,
                      'NOx': 0. * kg / t / km,
                      'PM10': 0. * kg / t / km
                      },
    'Road transport': {'CO2': 0.110 * kg / t / km,  # Binh & Tuan (2016)
                       # http://naei.defra.gov.uk/data/ef-transport, year 2014
                       'SO2': 0.003 * g / truck_economics['truck_load'] / km,
                       'NOx': 2.68 * g / truck_economics['truck_load'] / km,
                       'PM10': 0.04 * g / truck_economics['truck_load'] / km
                       },
    'Barge transport': {'CO2': 0.071 * kg / t / km,  # Binh & Tuan (2016)
                        # Van Dingenen et al. (2016)
                        'SO2': 2 * g / kg * barge_fuel_consumption,
                        'NOx': 50.75 * g / kg * barge_fuel_consumption,
                        'PM10': 3.19 * g / kg * barge_fuel_consumption}}

external_cost = pd.Series({'CO2': 1 * USD / t,
                           # Sakulniyomporn, Kubaha, and Chullabodhi (2011)
                           'SO2': 3767 * USD / t,
                           'PM10': 5883 * USD / t,
                           'NOx': 286 * USD / t
                           })


MongDuong1 = PowerPlant(name="Mong Duong 1",
                        capacity=1080 * MW * y,
                        capacity_factor=0.60,
                        commissioning=2015,
                        boiler_technology='CFB',
                        plant_efficiency=full(time_horizon + 1, 38.84 / 100),
                        boiler_efficiency=full(time_horizon + 1, 87.03 / 100),
                        fix_om_coal=29.31 * USD / kW / y,
                        variable_om_coal=0.0048 * USD / kWh,
                        emission_factor=emission_factor,
                        emission_control={'CO2': 0.0, 'SO2': 0.982, 'NOx': 0.0, 'PM10': 0.996},
                        coal=MD_Coal
                        )

MDSupplyZone1 = SupplyZone(shape=Semi_Annulus(0 * km, 50 * km),
                           straw_density=MongDuong1_straw_density1,
                           tortuosity_factor=1.5
                           )

MDSupplyZone2 = SupplyZone(shape=Semi_Annulus(50 * km, 100 * km),
                           straw_density=MongDuong1_straw_density2,
                           tortuosity_factor=1.5
                           )

MD_SupplyChain = SupplyChain(zones=[MDSupplyZone1, MDSupplyZone2],
                             straw_production=MongDuong1_straw_production,
                             straw_burn_rate=0.9,
                             average_straw_yield=MongDuong1_average_straw_yield)

Cofire_Tech = namedtuple('Cofire_Tech', ['biomass_ratio_energy',
                                         'capital_cost',
                                         'fix_om_cost',
                                         'variable_om_cost',
                                         'biomass',
                                         'boiler_efficiency_loss',
                                         'OM_hour_MWh',
                                         'wage_operation_maintenance'])


def boiler_efficiency_loss_function_T2000(biomass_ratio_mass):
    """Boiler efficiency loss due to cofiring, according to Tillman 2000"""
    return 0.0044 * biomass_ratio_mass**2 + 0.0055 * biomass_ratio_mass


cofire_MD1 = Cofire_Tech(biomass_ratio_energy=v_after_invest * 0.05,
                         capital_cost=50 * USD / kW / y,
                         fix_om_cost=32.24 * USD / kW / y,
                         variable_om_cost=0.006 * USD / kWh,
                         biomass=straw,
                         boiler_efficiency_loss=boiler_efficiency_loss_function_T2000,
                         OM_hour_MWh=0.12 * hr / MWh,  # working hour for OM per MWh
                         wage_operation_maintenance=1.67 * USD / hr
                         )

MongDuong1System = System(MongDuong1, cofire_MD1, MD_SupplyChain,
                          straw.price, emission_factor, collect_economics, truck_economics)


NinhBinh = PowerPlant(name="Ninh Binh",
                      capacity=100 * MW * y,
                      capacity_factor=0.64,
                      commissioning=1974,
                      boiler_technology='PC',
                      plant_efficiency=full(time_horizon + 1, 21.77 / 100),
                      boiler_efficiency=full(time_horizon + 1, 81.61 / 100),
                      fix_om_coal=29.31 * USD / kW / y,
                      variable_om_coal=0.0048 * USD / kWh,
                      emission_factor=emission_factor,
                      emission_control={'CO2': 0.0, 'SO2': 0.0, 'NOx': 0.0, 'PM10': 0.992},
                      coal=NB_Coal
                      )

NBSupplyZone = SupplyZone(shape=Disk(50 * km),
                          straw_density=NinhBinh_straw_density,
                          tortuosity_factor=1.5
                          )

NB_SupplyChain = SupplyChain(zones=[NBSupplyZone],
                             straw_production=NinhBinh_straw_production,
                             straw_burn_rate=0.9,
                             average_straw_yield=NinhBinh_average_straw_yield)

cofire_NB = cofire_MD1._replace(capital_cost=100 * USD / kW / y)

NinhBinhSystem = System(NinhBinh, cofire_NB, NB_SupplyChain,
                        straw.price, emission_factor, collect_economics, truck_economics)
