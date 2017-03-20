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

from emission import MD_transport, MD_field
from emission import MDCofire_transport, MDCofire_field, MD_ER_table

from emission import NB_transport, NB_field
from emission import NBCofire_transport, NBCofire_field, NB_ER_table

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire

print("\nMong Duong 1 BASELINE EMISSIONS\n")

print("Emissions from power plant\n", MongDuong1.stack.emissions().T, "\n")

print("Emissions from transport\n", MD_transport.emissions().T, "\n")

print("Emission from open field burning\n", MD_field.emissions().T, "\n")

print("-------\nMong Duong 1 COFIRING EMISSIONS\n")

print("Emissions from power plant\n", MongDuong1Cofire.stack.emissions().T, "\n")

print("Emissions from transport\n", MDCofire_transport.emissions().T, "\n")

print("Emission from open field burning\n", MDCofire_field.emissions().T, "\n")

print("-------\nMong Duong 1 EMISSION REDUCTION\n")

print(MD_ER_table, "\n")


print("==================\n")

print("\nNinh Binh BASELINE EMISSIONS\n")

print("Emissions from power plant\n", NinhBinh.stack.emissions().T, "\n")

print("Emissions from transport\n", NB_transport.emissions().T, "\n")

print("Emission from open field burning\n", NB_field.emissions().T, "\n")

print("-------\nNinh Binh COFIRING EMISSIONS\n")

print("Emission from power plant\n", NinhBinhCofire.stack.emissions().T, "\n")

print("Emissions from transportation\n", NBCofire_transport.emissions().T, "\n")

print("Emission from open field burning\n", NBCofire_field.emissions().T, "\n")

print("-------\nNinh Binh EMISSION REDUCTION")

print(NB_ER_table, "\n")

print("NEW table - move stack into PowerPlant class\n")


def print_plant_emission(plant, cofireplant):
    print(plant.name, 'BASELINE EMISSION')
    print('Emission from power plant')
    print(plant.stack.emissions().T, '\n')
    print('Emission from coal supply')
    print(plant.coal_transporter.emissions().T, '\n')
    print(plant.name, 'COFIRING EMISSION')
    print('Emission from power plant')
    print(cofireplant.stack.emissions().T, '\n')
    print('Emission from coal supply')
    print(cofireplant.coal_transporter.emissions().T, '\n')
    print('Emission from straw supply')
    print(cofireplant.straw_supply.transport_emissions().T, '\n')

print_plant_emission(MongDuong1, MongDuong1Cofire)
print_plant_emission(NinhBinh, NinhBinhCofire)
