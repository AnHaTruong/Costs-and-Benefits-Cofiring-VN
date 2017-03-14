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
from Emitter import Emitter
from strawburned import straw_burned_infield

from natu.units import t, km, y
import pandas as pd

print("\nMong Duong 1 BASELINE\n")

MD_plant_stack = Emitter({'6b_coal': MongDuong1.coal_used[1]},
                         emission_factor,
                         MD_controls)

print("Emissions from power plant\n", MD_plant_stack, "\n")

MD_transport = Emitter({'Road transport': 0 * t * km / y,
                        'Barge transport': 0 * t * km / y},
                       emission_factor,
                       {'CO2': 0.0}
                       )

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

print("From plant\n", MD_plant_stack.emissions["Total"] - MDCofire_plant_stack.emissions["Total"], "\n")
MD_stack_ER=pd.Series(MD_plant_stack.emissions["Total"] ['CO2'] -
                      MDCofire_plant_stack.emissions["Total"] ['CO2'], index=['CO2'])
MD_transport_ER = MD_transport.emissions["Total"] - MDCofire_transport.emissions["Total"]

print("From transportation")
print(MD_transport_ER, "\n")
print("From field\n", MD_field.emissions["Total"] - MDCofire_field.emissions["Total"], "\n")
print("Total emission reduction", MD_stack_ER + MD_transport_ER)


print("==================\n")

print("\nNinh Binh BASELINE\n")

NB_plant_stack = Emitter({'4b_coal': NinhBinh.coal_used[1]},
                         emission_factor,
                         NB_controls)

print("Emissions from power plant\n", NB_plant_stack, "\n")

NB_transport = Emitter({'Road transport' : 0 * t*km/y,
                        'Barge transport' :NB_Coal.transport_distance * 2 * NinhBinh.coal_used[1]},
                        emission_factor,
                        {'CO2' : 0.0})

print("Emissions from transport\n", NB_transport, "\n")

NB_field = Emitter({'Straw': straw_burned_infield(NinhBinh)},
                   emission_factor)

print("Emission from open field burning\n", NB_field, "\n")

print("-------\nNinh Binh COFIRING \n")

NBCofire_plant_stack = Emitter({'4b_coal': NinhBinhCofire.coal_used[1],
                                'Straw': NinhBinhCofire.biomass_used[1]},
                               emission_factor,
                               NB_controls)

print("Emission from power plant\n", NBCofire_plant_stack, "\n")

NBCofire_transport = Emitter({'Road transport' : NinhBinhCofire.active_chain.transport_tkm() / y,
                              'Barge transport' : NB_Coal.transport_distance * 2 * NinhBinhCofire.coal_used[1]},
                              emission_factor,
                              {'CO2' : 0.0})

print("Emissions from transportation\n", NBCofire_transport, "\n")

NBCofire_field = Emitter({'Straw': straw_burned_infield(NinhBinh) - NinhBinhCofire.biomass_used[1]},
                   emission_factor)

print("Emission from open field burning\n", NBCofire_field, "\n")

print("-------\nNinh Binh REDUCTION")

print("From plant\n", NB_plant_stack.emissions["Total"] - NBCofire_plant_stack.emissions["Total"], "\n")

NB_stack_ER=pd.Series(NB_plant_stack.emissions["Total"] ['CO2'] -
                      NBCofire_plant_stack.emissions["Total"] ['CO2'], index=['CO2'])
NB_transport_ER = NB_transport.emissions["Total"] - NBCofire_transport.emissions["Total"]

print("Reduction from transportation\n", NB_transport_ER, "\n")
print("Total emission reduction",NB_stack_ER + NB_transport_ER)
