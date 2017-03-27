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
from parameters import winder_haul, work_hour_day, OM_hour_MWh
from parameters import truck_load, truck_velocity, truck_loading_time

from job import v_benefit_bm_collection
from job import number_of_truck_trips, transport_time, v_benefit_bm_transport
from job import v_benefit_om, v_total_job_benefit
from job import v_benefit_bm_loading
print('')

cols = '{:25}{:12.1f}'
cols2 = '{:25}{:12.1f}{:12.1f}'


def print_job(plant, cofiringplant):
    print('Benefit from job creation:', plant.name, '\n')

    row1 = v_benefit_bm_collection(cofiringplant)[1]
    row2 = v_benefit_bm_transport(cofiringplant)[1]
    row3 = v_benefit_om(cofiringplant)[1]
    row7 = cofiringplant.straw_supply.farm_work(work_hour_day, winder_haul)[1]
    row8 = cofiringplant.straw_supply.transport_work(truck_load, truck_velocity)[1]
    row9 = cofiringplant.biomass_om_work(OM_hour_MWh)[1]
    row10 = cofiringplant.cofiring_work(OM_hour_MWh, work_hour_day, winder_haul,
                                        truck_load, truck_velocity, truck_loading_time)[1]
    row4 = v_total_job_benefit(plant, cofiringplant)[1]
    row11 = cofiringplant.straw_supply.loading_work(truck_loading_time)[1]
    row12 = v_benefit_bm_loading(cofiringplant)[1]

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
