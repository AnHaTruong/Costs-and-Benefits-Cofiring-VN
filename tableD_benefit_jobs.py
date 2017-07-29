# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Print table D for job created from co-firing in job.py.

TODO: rename the cells variables.
"""

from init import FTE, display_as

from parameters import MongDuong1System, NinhBinhSystem
from parameters import mining_parameter

print('')

cols = '{:25}{:12.1f}'
cols2 = '{:25}{:12.1f}{:12.1f}'


def print_job(system):
    """Print the number of full time equivalent (FTE) jobs created by cofiring."""
    print('Benefit from job creation:', system.plant.name, '\n')

    row7 = system.farmer.labor()[1]
    row1 = system.farmer.labor_cost()[1]
    row8 = system.transporter.driving_work()[1]
    row2 = system.transporter.driving_wages()[1]
    row11 = system.transporter.loading_work()[1]
    row12 = system.transporter.loading_wages()[1]
    row9 = system.cofiring_plant.biomass_om_work()[1]
    row3 = system.cofiring_plant.biomass_om_wages()[1]
    row10 = system.labor[1]
    row4 = system.wages[1]

    display_as(row7, 'FTE')
    display_as(row8, 'FTE')
    display_as(row9, 'FTE')
    display_as(row10, 'FTE')
    display_as(row11, 'FTE')

    print(cols2.format('Biomass collection', row7, row1))
    print(cols2.format('Biomass transportation', row8, row2))
    print(cols2.format('Biomass loading', row11, row12))
    print(cols2.format('O&M', row9, row3))
    print(cols2.format('Total', row10, row4))
    print()
    print(cols.format('Area collected', system.supply_chain.area()))
    print(cols.format('Collection radius', system.supply_chain.collection_radius()))
    print(cols.format('Maximum transport time', system.transporter.max_trip_time()))
    print(cols.format('Number of truck trips', system.transporter.truck_trips[1]))
    print()


def print_job_lost(system):
    """Print the number of full time equivalent (FTE) jobs destroyed by cofiring."""
    print('Mining job lost from co-firing at', system.plant.name, '\n')
    row = system.coal_work_lost(mining_parameter['productivity_underground'])[1]
    display_as(row, 'FTE')
    print(cols.format('Job lost', row))
    print(cols.format('Coal saved', system.coal_saved[1]))


print_job(MongDuong1System)
print_job_lost(MongDuong1System)
print('')
print_job(NinhBinhSystem)
print_job_lost(NinhBinhSystem)

print('Note: 1 FTE =', FTE)
