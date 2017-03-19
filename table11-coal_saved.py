# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Quantity and value of coal saved by co-firing.
"""

from parameters import MongDuong1Cofire, NinhBinhCofire, coal_import_price


def print_coal_saved(plant):
    col1 = plant.coal_saved[1]
    col2 = col1 * coal_import_price
    col2.display_unit = 'kUSD'

    row = '{:35}{:23.0f}'
    print('Coal saved at', plant.name)
    print(row.format('Amount of coal saved from co-firing', col1))
    print(row.format('Maximum benefit for trade balance', col2))

print_coal_saved(MongDuong1Cofire)

print('')

print_coal_saved(NinhBinhCofire)
