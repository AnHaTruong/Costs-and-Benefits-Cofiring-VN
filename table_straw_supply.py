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
"""Print table of the plant's technical parameters of the plants."""

from init import isclose
from parameters import MongDuong1System, NinhBinhSystem


def straw_supply(system_a, system_b):
    """Tabulate the straw requires and straw costs."""
    table = ["\nTable 5. Straw required and straw cost estimation\n"]

    col3 = system_a.cofiring_plant.biomass_used[1]
    col4 = system_b.cofiring_plant.biomass_used[1]

    col5 = system_a.cofiring_plant.biomass_cost_per_t()[1]
    col6 = system_b.cofiring_plant.biomass_cost_per_t()[1]

    col9 = MongDuong1System.transport_cost_per_t[1]
    col10 = NinhBinhSystem.transport_cost_per_t[1]

    assert isclose(col5 - col9, MongDuong1System.biomass_value[1] / col3)
    assert isclose(col6 - col10, NinhBinhSystem.biomass_value[1] / col4)

    table.append('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
    table.append('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
    table.append('{:24} {:>22.2f}{:>18.2f}'.format('Straw cost', col5, col6))
    table.append('{:24} {:>22.2f}{:>18.2f}'.format('Biomass raw cost', col5 - col9, col6 - col10))
    table.append('{:24} {:>19.2f}{:>18.2f}'.format('Biomass transportation cost', col9, col10))
    table.append('')
    table.append(system_a.plant.name + ' ' + str(system_a.supply_chain))
    table.append(system_b.plant.name + ' ' + str(system_b.supply_chain))

    return '\n'.join(table)


print(straw_supply(MongDuong1System, NinhBinhSystem))
