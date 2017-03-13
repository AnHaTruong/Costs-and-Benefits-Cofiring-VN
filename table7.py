# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Tests for the emission functions in  emission.py
"""

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import emission_factor, MD_controls
from Emitter import Emitter
from emission import emission_coal_combust_base, emission_coal_transport_base
from emission import emission_biomass_combust, emission_biomass_transport
from emission import total_emission_coal, total_emission_cofire
from emission import emission_reduction, emission_coal_combust_cofire
from emission import emission_coal_transport_cofire

print('')
row = '{:35}' + '{:16.2f}'


def print_emission(plant, cofiringplant):
    """Print table 7-Emission reduction from co-firing """

    col1 = emission_biomass_combust(plant) + emission_coal_combust_cofire(plant)
    col2 = emission_biomass_transport(cofiringplant) + emission_coal_transport_cofire(plant)
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
print('')


print("Mong Duong 1 baseline")
MD_plant_stack = Emitter({'6b_coal': MongDuong1.coal_consumption},
                         emission_factor,
                         MD_controls
                         )

print(MD_plant_stack, "\n")

print("Mong Duong 1 cofiring")
MDCofire_plant_stack = Emitter({'6b_coal': MongDuong1Cofire.coal_used()[1],
                                'Straw': MongDuong1Cofire.biomass_used[1]},
                               emission_factor,
                               MD_controls)

print(MDCofire_plant_stack, "\n")

print("Mong Duong 1 reduction")
print(MD_plant_stack.emissions["Total"] - MDCofire_plant_stack.emissions["Total"], "\n")


print("==================")

print('Greenhouse gas emission reduction NinhBinh')
print_emission(NinhBinh, NinhBinhCofire)


print("Ninh Binh baseline")
NB_plant_stack = Emitter({'6b_coal': NinhBinh.coal_consumption},
                         emission_factor
                         )

print(NB_plant_stack, "\n")

print("Ninh Binh cofire")
NBCofire_plant_stack = Emitter({'6b_coal': NinhBinhCofire.coal_used()[1],
                                'Straw': NinhBinhCofire.biomass_used[1]},
                               emission_factor
                               )

print(NBCofire_plant_stack, "\n")

print("Ninh Binh reduction")
print(NB_plant_stack.emissions["Total"] - NBCofire_plant_stack.emissions["Total"], "\n")
