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
""" Print table D for job created from co-firing in job.py
"""

from init import FTE, display_as
from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import collect_economics, truck_economics, OM_economics
from parameters import mining_productivity_underground

print('')

cols = '{:25}{:12.1f}'
cols2 = '{:25}{:12.1f}{:12.1f}'


def print_job(plant, cofiringplant):
    print('Benefit from job creation:', plant.name, '\n')

    row1 = cofiringplant.straw_supply.farm_wages(collect_economics)[1]
    row2 = cofiringplant.straw_supply.transport_wages(truck_economics)[1]
    row3 = cofiringplant.biomass_om_wages(OM_economics)[1]
    row7 = cofiringplant.straw_supply.farm_work(collect_economics)[1]
    row8 = cofiringplant.straw_supply.transport_work(truck_economics)[1]
    row9 = cofiringplant.biomass_om_work(OM_economics)[1]
    row10 = cofiringplant.cofiring_work(collect_economics, truck_economics, OM_economics)[1]
    row4 = cofiringplant.cofiring_wages(collect_economics, truck_economics, OM_economics)[1]
    row11 = cofiringplant.straw_supply.loading_work(truck_economics)[1]
    row12 = cofiringplant.straw_supply.loading_wages(truck_economics)[1]

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
    print(cols.format('Area collected', cofiringplant.straw_supply.area()))
    print(cols.format('Collection radius', cofiringplant.straw_supply.collection_radius()))
    print(cols.format('Truck trips: duration',
                      cofiringplant.straw_supply.transport_time(truck_economics)
                      )
          )
    truck_trips = cofiringplant.biomass_used[1] / truck_economics['truck_load']
    print(cols.format('Truck trips: number', truck_trips))
    print()


def print_job_lost(plant, cofiringplant):
    print('Mining job lost from co-firing at', plant.name, '\n')
    row = cofiringplant.coal_work_lost(mining_productivity_underground)[1]
    display_as(row, 'FTE')
    print(cols.format('Job lost', row))
    print(cols.format('Coal saved', cofiringplant.coal_saved[1]))


print_job(MongDuong1, MongDuong1Cofire)
print_job_lost(MongDuong1, MongDuong1Cofire)
print('')
print_job(NinhBinh, NinhBinhCofire)
print_job_lost(NinhBinh, NinhBinhCofire)

print('Note: 1 FTE =', FTE)
