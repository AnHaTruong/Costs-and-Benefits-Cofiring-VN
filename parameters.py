
# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
import pandas as pd

from init import USD, VND, time_horizon
from natu.units import MJ, kg, t, d, hr, km, MW, ha, kW, y, kWh
from natu.numpy import full

from strawdata import MongDuong1_straw_density1, MongDuong1_straw_density2
from strawdata import NinhBinh_straw_density, NinhBinh_straw_production
from strawdata import MongDuong1_straw_production1, MongDuong1_straw_production2

from Emitter import Fuel
from PowerPlant import PowerPlant, CofiringPlant
from Shape import Semi_Annulus, Disk
from SupplyChain import SupplyChain, SupplyZone


"""Input parameters of the model"""

discount_rate = 0.087771
depreciation_period = 10
tax_rate = 0.25  # Corporate tax in Vietnam
feedin_tarif = {'MD': 1239.17 * VND / kWh, 'NB': 1665.6 * VND / kWh}

biomass_ratio = 0.05           # As percent of energy coming from biomass


def boiler_efficiency_loss(biomass_ratio_mass):
    """Boiler efficiency loss due to cofiring, according to Tillman 2000"""
    return 0.0044 * biomass_ratio_mass**2 + 0.0055 * biomass_ratio_mass

straw_burn_rate = 0.9  # Percentage of straw burned infield after harvest
winder_haul = 6.57 * t / d
work_hour_day = 8 * hr / d
truck_velocity = 45 * km / hr
truck_load = 20 * t
OM_hour_MWh = 0.12 * hr / MW / hr  # working hour for OM per MWh    # O&M of co-firing per MWh

transport_tariff = 2000 * VND / t / km  # vantaiduongviet.com
tortuosity_factor = 1.5
# wage per hour is calculated from base salary defined in governmental regulations
wage_bm_collect = 1.11 * USD / hr
wage_bm_transport = 1.11 * USD / hr
wage_operation_maintenance = 1.67 * USD / hr
winder_rental_cost = 40 * USD / ha   # per period

coal_import_price = 73 * USD / t

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
    '6b_coal': {'CO2': 0.0966 * kg / MJ * MD_Coal.heat_value,
                'SO2': 11.5 * kg / t,
                'NOx': 18 * kg / t,
                'PM10': 43.8 * kg / t
                },
    '4b_coal': {'CO2': 0.0966 * kg / MJ * NB_Coal.heat_value,
                'SO2': 11.5 * kg / t,
                'NOx': 18 * kg / t,
                'PM10': 26.1 * kg / t
                },
    'Straw': {'CO2': 0.0858 * kg / MJ * straw.heat_value,
              'SO2': 0.18 * kg / t,
              'NOx': 2.28 * kg / t,
              'PM10': 9.1 * kg / t
              },
    'Conveyor belt': {'CO2': 0.0 * kg / t / km,
                      'SO2': 0. * kg / t / km,
                      'NOx': 0. * kg / t / km,
                      'PM10': 0. * kg / t / km
                      },
    'Road transport': {'CO2': 0.110 * kg / t / km,
                       'SO2': 0. * kg / t / km,
                       'NOx': 0. * kg / t / km,
                       'PM10': 0. * kg / t / km
                       },
    'Barge transport': {'CO2': 0.071 * kg / t / km,
                        'SO2': 0. * kg / t / km,
                        'NOx': 0. * kg / t / km,
                        'PM10': 0. * kg / t / km}}

specific_cost = pd.Series({'CO2': 1 * USD / t,
                           'SO2': 3767 * USD / t,
                           'PM10': 5883 * USD / t,
                           'NOx': 286 * USD / t
                           })

MongDuong1 = PowerPlant(name="Mong Duong 1",
                        capacity=1080 * MW,
                        capacity_factor=0.60,
                        commissioning=2015,
                        boiler_technology='CFB',
                        plant_efficiency=full(time_horizon + 1, 38.84 / 100),
                        boiler_efficiency=full(time_horizon + 1, 87.03 / 100),
                        fix_om_coal=29.31 * USD / kW / y,
                        variable_om_coal=0.0048 * USD / kWh,
                        emission_controls={'CO2': 0.0, 'SO2': 0.982, 'NOx': 0.0, 'PM10': 0.996},
                        emission_factor=emission_factor,
                        coal=MD_Coal
                        )

MDSupplyZone1 = SupplyZone(shape=Semi_Annulus(0 * km, 50 * km),
                           straw_density=MongDuong1_straw_density1,
                           straw_production=MongDuong1_straw_production1,
                           straw_burn_rate=straw_burn_rate,
                           transport_tariff=transport_tariff,
                           tortuosity_factor=tortuosity_factor
                           )

MDSupplyZone2 = SupplyZone(shape=Semi_Annulus(50 * km, 100 * km),
                           straw_density=MongDuong1_straw_density2,
                           transport_tariff=transport_tariff,
                           straw_production=MongDuong1_straw_production2,
                           straw_burn_rate=straw_burn_rate,
                           tortuosity_factor=tortuosity_factor
                           )

MD_SupplyChain = SupplyChain(zones=[MDSupplyZone1, MDSupplyZone2], emission_factor=emission_factor)

MongDuong1Cofire = CofiringPlant(MongDuong1,
                                 biomass_ratio,
                                 capital_cost=50 * USD / kW,
                                 fix_om_cost=32.24 * USD / kW / y,
                                 variable_om_cost=0.006 * USD / (kW * hr),
                                 biomass=straw,
                                 boiler_efficiency_loss=boiler_efficiency_loss,
                                 supply_chain=MD_SupplyChain
                                 )

NinhBinh = PowerPlant(name="Ninh Binh",
                      capacity=100 * MW,
                      capacity_factor=0.64,
                      commissioning=1974,
                      boiler_technology='PC',
                      plant_efficiency=full(time_horizon + 1, 21.77 / 100),
                      boiler_efficiency=full(time_horizon + 1, 81.61 / 100),
                      fix_om_coal=29.31 * USD / kW / y,
                      variable_om_coal=0.0048 * USD / kWh,
                      emission_controls={'CO2': 0.0, 'SO2': 0.0, 'NOx': 0.0, 'PM10': 0.992},
                      emission_factor=emission_factor,
                      coal=NB_Coal
                      )

NBSupplyZone = SupplyZone(shape=Disk(50 * km),
                          straw_density=NinhBinh_straw_density,
                          straw_production=NinhBinh_straw_production,
                          straw_burn_rate=straw_burn_rate,
                          transport_tariff=transport_tariff,
                          tortuosity_factor=tortuosity_factor
                          )

NB_SupplyChain = SupplyChain(zones=[NBSupplyZone], emission_factor=emission_factor)

NinhBinhCofire = CofiringPlant(NinhBinh,
                               biomass_ratio,
                               capital_cost=100 * USD / kW,
                               fix_om_cost=32.24 * USD / kW / y,
                               variable_om_cost=0.006 * USD / (kW * hr),
                               biomass=straw,
                               boiler_efficiency_loss=boiler_efficiency_loss,
                               supply_chain=NB_SupplyChain
                               )
