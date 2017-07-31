# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Print table 1 for Technical parameters of the plants."""

from natu.units import y

from parameters import MongDuong1System, NinhBinhSystem


def technical_parameters(system_a, system_b):
    """Tabulate the technical parameters for two plants."""
    plant_a = system_a.plant
    plant_b = system_b.plant
    table = ['\nTable 1. Technical parameters\n']

    table.append('{:24}{:>20}{:>20}'.format('Parameter', plant_a.name, plant_b.name))

    table.append('{:24}{:>20}{:>20}'.format('Comissioning year',
                                            plant_a.parameter.commissioning,
                                            plant_b.parameter.commissioning))

    table.append('{:24}{:>20}{:>20}'.format('Boiler technology',
                                            plant_a.parameter.boiler_technology,
                                            plant_b.parameter.boiler_technology))

    table.append('{:24}{:>20.0f}{:>17.0f}'.format('Installed capacity',
                                                  plant_a.parameter.capacity / y,
                                                  plant_b.parameter.capacity / y))

    table.append('{:24}{:>20.2f}{:>20.2f}'.format('Capacity factor',
                                                  plant_a.parameter.capacity_factor,
                                                  plant_b.parameter.capacity_factor))

    table.append('{:24}{:>20.0f}{:>16.0f}'.format('Coal consumption',
                                                  plant_a.coal_used[0],
                                                  plant_b.coal_used[0]))

    table.append('{:24}{:>20.0f}{:>14.0f}'.format('Heat value of coal',
                                                  plant_a.parameter.coal.heat_value,
                                                  plant_b.parameter.coal.heat_value))

    table.append('{:24}{:>20.4f}{:>20.4f}'.format('Plant efficiency',
                                                  plant_a.           plant_efficiency[0],
                                                  plant_b.           plant_efficiency[0]))

    table.append('{:24}{:>20.4f}{:>20.4f}'.format('Boiler efficiency',
                                                  plant_a.parameter.boiler_efficiency[0],
                                                  plant_b.parameter.boiler_efficiency[0]))

    return '\n'.join(table)


print(technical_parameters(MongDuong1System, NinhBinhSystem))
