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
from emission import emission_coal_combust_base, emission_coal_transport_base
from emission import emission_biomass_combust, emission_biomass_transport
from emission import total_emission_coal, total_emission_cofire
from emission import emission_reduction, emission_coal_combust_cofire
from emission import emission_coal_transport_cofire
from strawburned import straw_burned_infield

from units import isclose
from natu.units import t, km, y
import pandas as pd

print('')
row = '{:35}' + '{:16.2f}'


def print_emission(plant, cofiringplant):
    """Print table 7-Emission reduction from co-firing """

    col1 = emission_biomass_combust(plant, cofiringplant) + emission_coal_combust_cofire(plant, cofiringplant)
    col2 = emission_biomass_transport(cofiringplant) + emission_coal_transport_cofire(plant, cofiringplant)
    col3 = total_emission_cofire(plant, cofiringplant)
    col4 = emission_coal_combust_base(plant)
    col5 = emission_coal_transport_base(plant)
    col6 = total_emission_coal(plant)
    col7 = emission_reduction(plant, cofiringplant)

    col1.display_unit = 't/y'
    col2.display_unit = 't/y'
    col3.display_unit = 't/y'
    col4.display_unit = 't/y'
    col5.display_unit = 't/y'
    col6.display_unit = 't/y'
    col7.display_unit = 't/y'

    print(row.format('Emission from combustion baseline', col4))
    print(row.format('Emission from transport baseline', col5))
    print(row.format('Emission from combustion co-firing', col1))
    print(row.format('Emission from transport co-firing', col2))
    print(row.format('Emission baseline case', col6))
    print(row.format('Emission co-firing case', col3))
    print(row.format('Emission reduction', col7))

print('Greenhouse gas emission reduction Mong Duong 1')
print_emission(MongDuong1, MongDuong1Cofire)

print("\nMong Duong 1 BASELINE\n")

MD_plant_stack = Emitter({'6b_coal': MongDuong1.coal_used[1]},
                         emission_factor,
                         MD_controls)

assert isclose(MD_plant_stack.emissions['Total']['CO2'], emission_coal_combust_base(MongDuong1))

print("Emissions from power plant\n", MD_plant_stack, "\n")

MD_transport = Emitter({'Road transport' : 0 * t*km/y,
                        'Barge transport' : 0 * t*km /y},
                        emission_factor,
                        {'CO2' : 0.0})
                        
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

assert isclose(MDCofire_plant_stack.emissions['Total']['CO2'],
               emission_biomass_combust(MongDuong1, MongDuong1Cofire) +
               emission_coal_combust_cofire(MongDuong1, MongDuong1Cofire))

MDCofire_transport = Emitter({'Road transport' : MongDuong1Cofire.active_chain.transport_tkm() /y,
                              'Barge transport' : 0 * t*km /y},
                              emission_factor,
                              {'CO2' : 0.0})
                              
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

print('Greenhouse gas emission reduction NinhBinh')
print_emission(NinhBinh, NinhBinhCofire)

print("\nNinh Binh BASELINE\n")

NB_plant_stack = Emitter({'4b_coal': NinhBinh.coal_used[1]},
                         emission_factor,
                         NB_controls)

print("Emissions from power plant\n", NB_plant_stack, "\n")

assert isclose(NB_plant_stack.emissions['Total']['CO2'], emission_coal_combust_base(NinhBinh))

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
                               
assert isclose(NBCofire_plant_stack.emissions['Total']['CO2'],
               emission_biomass_combust(NinhBinh, NinhBinhCofire) +
               emission_coal_combust_cofire(NinhBinh, NinhBinhCofire))
                               
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
