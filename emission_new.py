# Economic of co-firing in two power plants in Vietnam
#
#  Greenhouse gas emissions reduction assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Greenhouse gas and pollutant emissions assessment of a co-firing project.
   Total emission include emission from fuel combustion, fuel transportation and open field burning
   Climate benefit and health benefit from GHG and air pollutant emission reduction
"""
from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import emission_factor, MD_controls
from parameters import NB_controls, NB_Coal
from parameters import specific_cost
from Emitter import Emitter
from strawburned import straw_burned_infield

import pandas as pd
#from units import isclose
from natu.units import t, km, y

MD_plant_stack = Emitter({'6b_coal': MongDuong1.coal_used[1]},
                         emission_factor,
                         MD_controls)

MD_transport = Emitter({'Road transport': 0 * t * km / y, 'Barge transport': 0 * t * km / y},
                       emission_factor,
                       {'CO2': 0.0})

MD_field = Emitter({'Straw': straw_burned_infield(MongDuong1)},
                   emission_factor)

MDCofire_plant_stack = Emitter({'6b_coal': MongDuong1Cofire.coal_used[1],
                                'Straw': MongDuong1Cofire.biomass_used[1]},
                               emission_factor,
                               MD_controls)

MDCofire_transport = Emitter({'Road transport': MongDuong1Cofire.active_chain.transport_tkm() / y,
                             'Barge transport': 0 * t * km / y
                              },
                             emission_factor,
                             {'CO2': 0.0}
                             )

MDCofire_field = Emitter({'Straw': straw_burned_infield(MongDuong1) - MongDuong1Cofire.biomass_used[1]},
                         emission_factor)

MD_plant_ER = MD_plant_stack.emissions["Total"] - MDCofire_plant_stack.emissions["Total"]

MD_transport_CO2 = MD_transport.emissions["Total"] - MDCofire_transport.emissions["Total"]
MD_transport_pollutant = pd.Series([0.0 * t / y, 0.0 * t / y, 0.0 * t / y],
                                   index=['SO2', 'PM10', 'NOx'])
MD_transport_ER = MD_transport_CO2.append(MD_transport_pollutant)

MD_field_ER = MD_field.emissions["Total"] - MDCofire_field.emissions["Total"]

MD_total_ER = MD_plant_ER + MD_transport_ER + MD_field_ER

MD_total_benefit = MD_total_ER * specific_cost

MD_ER_benefit = MD_total_benefit['CO2']
MD_health_benefit = MD_total_benefit.drop('CO2').sum()


NB_plant_stack = Emitter({'4b_coal': NinhBinh.coal_used[1]},
                         emission_factor,
                         NB_controls)

NB_transport = Emitter({'Road transport': 0 * t * km / y,
                        'Barge transport': NB_Coal.transport_distance * 2 * NinhBinh.coal_used[1]
                        },
                       emission_factor,
                       {'CO2': 0.0}
                       )
NB_field = Emitter({'Straw': straw_burned_infield(NinhBinh)},
                   emission_factor)

NBCofire_plant_stack = Emitter({'4b_coal': NinhBinhCofire.coal_used[1],
                                'Straw': NinhBinhCofire.biomass_used[1]},
                               emission_factor,
                               NB_controls)

NBCofire_transport = Emitter({'Road transport': NinhBinhCofire.active_chain.transport_tkm() / y,
                              'Barge transport': NB_Coal.transport_distance * 2 * NinhBinhCofire.coal_used[1]},
                             emission_factor,
                             {'CO2': 0.0})

NBCofire_field = Emitter({'Straw': straw_burned_infield(NinhBinh) - NinhBinhCofire.biomass_used[1]},
                         emission_factor)

NB_plant_ER = NB_plant_stack.emissions["Total"] - NBCofire_plant_stack.emissions["Total"]

NB_transport_CO2 = NB_transport.emissions["Total"] - NBCofire_transport.emissions["Total"]
NB_transport_pollutant = pd.Series([0.0 * t / y, 0.0 * t / y, 0.0 * t / y],
                                   index=['SO2', 'PM10', 'NOx'])
NB_transport_ER = NB_transport_CO2.append(NB_transport_pollutant)

NB_field_ER = NB_field.emissions["Total"] - NBCofire_field.emissions["Total"]
NB_total_ER = NB_plant_ER + NB_transport_ER + NB_field_ER

NB_total_benefit = NB_total_ER * specific_cost
NB_ER_benefit = NB_total_benefit['CO2']
NB_health_benefit = NB_total_benefit.drop('CO2').sum()
