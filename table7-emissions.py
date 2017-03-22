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
from emission import emission_reduction


def print_emission(plant, cofireplant):
    print(plant.name, 'BASELINE EMISSION')
    print('Emission from power plant')
    print(plant.stack.emissions().T, '\n')
    print('Emission from coal supply')
    print(plant.coal_transporter().emissions().T, '\n')
    print('Emission from open field burning')
    print(cofireplant.straw_supply.field_emission(cofireplant.biomass_used[0]).T, '\n')
    print(plant.name, 'COFIRING EMISSION')
    print('Emission from power plant')
    print(cofireplant.stack.emissions().T, '\n')
    print('Emission from coal supply')
    print(cofireplant.coal_transporter().emissions().T, '\n')
    print('Emission from straw supply')
    print(cofireplant.straw_supply.transport_emissions().T, '\n')
    print('Emission from open field burning')
    print(cofireplant.straw_supply.field_emission(cofireplant.biomass_used).T, '\n')


print_emission(MongDuong1, MongDuong1Cofire)
print("-------\nMong Duong 1 EMISSION REDUCTION\n")
print(emission_reduction(MongDuong1, MongDuong1Cofire))

print("==================\n")

print_emission(NinhBinh, NinhBinhCofire)
print("-------\nNinh Binh EMISSION REDUCTION")
print(emission_reduction(NinhBinh, NinhBinhCofire))
