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

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import specific_cost


def table(emission_df):
    print(emission_df.applymap(lambda v: v[1]).T, '\n')


def print_emission(plant, cofireplant):
    print(plant.name, 'BASELINE EMISSION')
    print('Emission from power plant')
    table(plant.stack.emissions())
    print('Emission from coal supply')
    table(plant.coal_transporter().emissions())
    print('Emission from open field burning')
    table(cofireplant.straw_supply.field_emission(cofireplant.biomass_used[0]))
    print(plant.name, 'COFIRING EMISSION')
    print('Emission from power plant')
    table(cofireplant.stack.emissions())
    print('Emission from coal supply')
    table(cofireplant.coal_transporter().emissions())
    print('Emission from straw supply')
    table(cofireplant.straw_supply.transport_emissions())
    print('Emission from open field burning')
    table(cofireplant.straw_supply.field_emission(cofireplant.biomass_used))
    print('-------')
    print(plant.name, 'EMISSION REDUCTION\n')
    table(cofireplant.emission_reduction(specific_cost).T)


print_emission(MongDuong1, MongDuong1Cofire)
print('==================\n')

print_emission(NinhBinh, NinhBinhCofire)
