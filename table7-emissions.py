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
"""Tabulate annual emissions rate of different pollutants, without and with cofiring."""

from parameters import MongDuong1System, NinhBinhSystem
from parameters import external_cost


def table(emission_df):
    """Print a dataframe containing time series, showing only the second item of each element.

    Assumes that investment occured in period 0, so period 1 is the rate with cofiring.
    """
    print(emission_df.applymap(lambda v: v[1]).T, '\n')


def print_emission(system):
    """Print the various emissions tables.

    There are many tables because:
        Emissions come from the plant, the supply, the straw supply, the open field burning
        Emissions can be  without cofiring / with cofiring / the difference
    """
    cofireplant = system.cofiring_plant
    plant = system.plant
    print(plant.name, 'BASELINE EMISSION')
    print('Emission from power plant')
    table(plant.emissions())
    print('Emission from coal supply')
    table(plant.coal_transporter().emissions())
    print('Emission from open field burning')
    table(system.farmer.emissions_exante)
    print(plant.name, 'COFIRING EMISSION')
    print('Emission from power plant')
    table(cofireplant.emissions())
    print('Emission from coal supply')
    table(cofireplant.coal_transporter().emissions())
    print('Emission from straw supply')
    table(system.transporter.emissions())
    print('Emission from open field burning')
    table(system.farmer.emissions())
    print('-------')
    print(plant.name, 'EMISSION REDUCTION\n')
    table(system.emission_reduction(external_cost).T)


print_emission(MongDuong1System)

print("==================\n")

print_emission(NinhBinhSystem)
