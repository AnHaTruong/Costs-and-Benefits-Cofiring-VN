# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Regression testing : Emitter.py  vs.  emission.py
"""

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import emission_factor, MD_controls
from parameters import NB_controls, NB_Coal
from parameters import specific_cost
from Emitter import Emitter
from emission import emission_coal_combust_base
from emission import emission_biomass_combust
from emission import emission_coal_combust_cofire
from strawburned import straw_burned_infield

import pandas as pd
from units import isclose, display_as
from natu.units import t, km, y

print("\nMong Duong 1 BASELINE\n")

MD_plant_stack = Emitter({'6b_coal': MongDuong1.coal_used[1]},
                         emission_factor,
                         MD_controls)

print("Emissions from power plant\n", MD_plant_stack, "\n")

MD_transport = Emitter({'Road transport': 0 * t * km / y, 'Barge transport': 0 * t * km / y},
                       emission_factor,
                       {'CO2': 0.0})

print("Emissions from transport\n", MD_transport, "\n")

MD_field = Emitter({'Straw': straw_burned_infield(MongDuong1)},
                   emission_factor)

print("Emission from open field burning\n", MD_field, "\n")

print("-------\nMong Duong 1 COFIRING\n")

MDCofire_plant_stack = Emitter({'6b_coal': MongDuong1Cofire.coal_used[1],
                                'Straw': MongDuong1Cofire.biomass_used[1]},
                               emission_factor,
                               MD_controls)

print("Emissions from power plant\n", MDCofire_plant_stack, "\n")


MDCofire_transport = Emitter({'Road transport': MongDuong1Cofire.active_chain.transport_tkm() / y,
                             'Barge transport': 0 * t * km / y
                              },
                             emission_factor,
                             {'CO2': 0.0}
                             )

print("Emissions from transport\n", MDCofire_transport, "\n")

MDCofire_field = Emitter({'Straw': straw_burned_infield(MongDuong1) - MongDuong1Cofire.biomass_used[1]},
                         emission_factor)

print("Emission from open field burning\n", MDCofire_field, "\n")

print("-------\nMong Duong 1 REDUCTION\n")

MD_plant_ER = MD_plant_stack.emissions["Total"] - MDCofire_plant_stack.emissions["Total"]
print("From plant\n", MD_plant_ER, "\n")

MD_transport_CO2 = MD_transport.emissions["Total"] - MDCofire_transport.emissions["Total"]
MD_transport_pollutant = pd.Series([0.0 * t / y, 0.0 * t / y, 0.0 * t / y],
                                   index=['SO2', 'PM10', 'NOx'])
MD_transport_ER = MD_transport_CO2.append(MD_transport_pollutant)
print("From transport\n", MD_transport_ER, "\n")

MD_field_ER = MD_field.emissions["Total"] - MDCofire_field.emissions["Total"]
print("From field\n", MD_field_ER, "\n")

MD_total_ER = MD_plant_ER + MD_transport_ER + MD_field_ER
print("Total emission reduction pollutants \n", MD_total_ER, "\n")

MD_total_benefit = MD_total_ER * specific_cost
print("Benefit\n", display_as(MD_total_benefit, 'kUSD/y'))


print("==================\n")

print("\nNinh Binh BASELINE\n")

NB_plant_stack = Emitter({'4b_coal': NinhBinh.coal_used[1]},
                         emission_factor,
                         NB_controls)

print("Emissions from power plant\n", NB_plant_stack, "\n")

assert isclose(NB_plant_stack.emissions['Total']['CO2'], emission_coal_combust_base(NinhBinh))

NB_transport = Emitter({'Road transport': 0 * t * km / y,
                        'Barge transport': NB_Coal.transport_distance * 2 * NinhBinh.coal_used[1]
                        },
                       emission_factor,
                       {'CO2': 0.0}
                       )

print("Emissions from transport\n", NB_transport, "\n")

NB_field = Emitter({'Straw': straw_burned_infield(NinhBinh)},
                   emission_factor)

print("Emission from open field burning\n", NB_field, "\n")

print("-------\nNinh Binh COFIRING \n")

NBCofire_plant_stack = Emitter({'4b_coal': NinhBinhCofire.coal_used[1],
                                'Straw': NinhBinhCofire.biomass_used[1]},
                               emission_factor,
                               NB_controls)

assert isclose(NBCofire_plant_stack.emissions['Total']['CO2'],
               emission_biomass_combust(NinhBinhCofire)
               + emission_coal_combust_cofire(NinhBinhCofire))

print("Emission from power plant\n", NBCofire_plant_stack, "\n")

NBCofire_transport = Emitter({'Road transport': NinhBinhCofire.active_chain.transport_tkm() / y,
                              'Barge transport': NB_Coal.transport_distance * 2 * NinhBinhCofire.coal_used[1]},
                             emission_factor,
                             {'CO2': 0.0})

print("Emissions from transportation\n", NBCofire_transport, "\n")

NBCofire_field = Emitter({'Straw': straw_burned_infield(NinhBinh) - NinhBinhCofire.biomass_used[1]},
                         emission_factor)

print("Emission from open field burning\n", NBCofire_field, "\n")

print("-------\nNinh Binh REDUCTION")

NB_plant_ER = NB_plant_stack.emissions["Total"] - NBCofire_plant_stack.emissions["Total"]
print("From plant\n", NB_plant_ER, "\n")

NB_transport_CO2 = NB_transport.emissions["Total"] - NBCofire_transport.emissions["Total"]
NB_transport_pollutant = pd.Series([0.0 * t / y, 0.0 * t / y, 0.0 * t / y],
                                   index=['SO2', 'PM10', 'NOx'])
NB_transport_ER = NB_transport_CO2.append(NB_transport_pollutant)
print("From transport\n", NB_transport_ER, "\n")

NB_field_ER = NB_field.emissions["Total"] - NBCofire_field.emissions["Total"]
print("From field\n", NB_field_ER, "\n")

NB_total_ER = NB_plant_ER + NB_transport_ER + NB_field_ER
print("Total emission reduction pollutants \n", NB_total_ER, "\n")

NB_total_benefit = NB_total_ER * specific_cost

print("Benefit\n", display_as(NB_total_benefit, 'kUSD/y'))
