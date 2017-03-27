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

from job import bm_collection_work, bm_transport_work, benefit_bm_collection
from job import number_of_truck_trips, transport_time, benefit_bm_transport
from job import om_work, cofiring_work, benefit_om, total_job_benefit
from job import benefit_bm_loading, bm_loading_work
print('')

cols = '{:25}{:12.1f}'
cols2 = '{:25}{:12.1f}{:12.1f}'


def print_job(plant, cofiringplant):
    print('Benefit from job creation:', plant.name, '\n')

    row1 = benefit_bm_collection(cofiringplant)
    row2 = benefit_bm_transport(cofiringplant)[1]
    row3 = benefit_om(plant)
    row7 = bm_collection_work(cofiringplant)
    row8 = bm_transport_work(cofiringplant)[1]
    row9 = om_work(plant)
    row10 = cofiring_work(plant, cofiringplant)
    row4 = total_job_benefit(plant, cofiringplant)
    row11 = bm_loading_work(cofiringplant)
    row12 = benefit_bm_loading(cofiringplant)

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
    print(cols.format('Truck trips: duration', transport_time(cofiringplant)))
    print(cols.format('Truck trips: number', number_of_truck_trips(cofiringplant)))
    print()

print_job(MongDuong1, MongDuong1Cofire)

print_job(NinhBinh, NinhBinhCofire)

print('Note: 1 FTE =', FTE)
