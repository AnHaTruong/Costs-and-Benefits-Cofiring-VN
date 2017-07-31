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


def as_table(emission_df):
    """Print a dataframe containing time series, showing only the second item of each element.

    Assumes that investment occured in period 0, so period 1 is the rate with cofiring.
    """
    return str(emission_df.applymap(lambda v: v[1]).T) + '\n'


def emissions(system):
    """Print the various emissions tables.

    There are many tables because:
        Emissions come from the plant, the supply, the straw supply, the open field burning
        Emissions can be  without cofiring / with cofiring / the difference
    """
    cofireplant = system.cofiring_plant
    plant = system.plant
    table = []
    table.append(plant.name + ' BASELINE EMISSION')
    table.append('Emission from power plant')
    table.append(as_table(plant.emissions()))
    table.append('Emission from coal supply')
    table.append(as_table(plant.coal_transporter().emissions()))
    table.append('Emission from open field burning')
    table.append(as_table(system.farmer.emissions_exante))
    table.append(plant.name + ' COFIRING EMISSION')
    table.append('Emission from power plant')
    table.append(as_table(cofireplant.emissions()))
    table.append('Emission from coal supply')
    table.append(as_table(cofireplant.coal_transporter().emissions()))
    table.append('Emission from straw supply')
    table.append(as_table(system.transporter.emissions()))
    table.append('Emission from open field burning')
    table.append(as_table(system.farmer.emissions()))
    table.append('-------')
    table.append(plant.name + ' EMISSION REDUCTION\n')
    table.append(as_table(system.emission_reduction(external_cost).T))
    return '\n'.join(table)


print(emissions(MongDuong1System))

print("==================\n")

print(emissions(NinhBinhSystem))
