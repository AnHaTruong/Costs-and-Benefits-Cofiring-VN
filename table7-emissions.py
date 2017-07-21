# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#  Results table: Emissions, emission reduction, health benefits
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

from parameters import MongDuong1System, NinhBinhSystem
from parameters import specific_cost


def table(emission_df):
    print(emission_df.applymap(lambda v: v[1]).T, '\n')


def print_emission(system):
    #TODO: use the emissions before/after invest instead of comparing the two plants
    cofireplant = system.cofiring_plant
    plant = cofireplant.plant
    print(plant.name, 'BASELINE EMISSION')
    print('Emission from power plant')
    table(plant.stack.emissions())
    print('Emission from coal supply')
    table(plant.coal_transporter().emissions())
    print('Emission from open field burning')
    table(system.farmer.emissions_exante)
    print(plant.name, 'COFIRING EMISSION')
    print('Emission from power plant')
    table(cofireplant.stack.emissions())
    print('Emission from coal supply')
    table(cofireplant.coal_transporter().emissions())
    print('Emission from straw supply')
    table(system.transporter.emissions())
    print('Emission from open field burning')
    table(system.farmer.emissions())
    print('-------')
    print(plant.name, 'EMISSION REDUCTION\n')
    table(system.emission_reduction(specific_cost).T)


print_emission(MongDuong1System)
print("==================\n")

print_emission(NinhBinhSystem)
