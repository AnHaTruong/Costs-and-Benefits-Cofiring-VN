# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Print quantity and value of coal saved by co-firing."""

from init import display_as
from parameters import MongDuong1System, NinhBinhSystem, coal_import_price


def coal_saved(system):
    """Tabulate the quantity and value of coal saved by cofiring."""
    col1 = system.coal_saved[1]
    col2 = display_as(col1 * coal_import_price, 'kUSD')

    row = '{:35}{:23.0f}'
    table = ['Coal saved at ' + str(system.cofiring_plant.name)]
    table.append(row.format('Amount of coal saved from co-firing', col1))
    table.append(row.format('Maximum benefit for trade balance', col2))
    return '\n'.join(table)


print(coal_saved(MongDuong1System))
print('')
print(coal_saved(NinhBinhSystem))
