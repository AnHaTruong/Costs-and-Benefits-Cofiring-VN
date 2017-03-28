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
from parameters import winder_haul, work_hour_day, wage_bm_collect
from parameters import truck_load, truck_velocity, wage_bm_transport
from parameters import truck_loading_time, wage_bm_loading
from parameters import OM_hour_MWh, wage_operation_maintenance

print('')

cols = '{:25}{:12.1f}'
cols2 = '{:25}{:12.1f}{:12.1f}'


def print_job(plant, cofiringplant):
    print('Benefit from job creation:', plant.name, '\n')

    row1 = cofiringplant.straw_supply.farm_wages(work_hour_day, winder_haul, wage_bm_collect)[1]
    row2 = cofiringplant.straw_supply.transport_wages(truck_load,
                                                      truck_velocity,
                                                      wage_bm_transport)[1]
    row3 = cofiringplant.biomass_om_wages(OM_hour_MWh, wage_operation_maintenance)[1]
    row7 = cofiringplant.straw_supply.farm_work(work_hour_day, winder_haul)[1]
    row8 = cofiringplant.straw_supply.transport_work(truck_load, truck_velocity)[1]
    row9 = cofiringplant.biomass_om_work(OM_hour_MWh)[1]
    row10 = cofiringplant.cofiring_work(OM_hour_MWh, work_hour_day, winder_haul,
                                        truck_load, truck_velocity, truck_loading_time)[1]
    row4 = cofiringplant.cofiring_wages(work_hour_day,
                                        winder_haul,
                                        wage_bm_collect,
                                        truck_load,
                                        truck_velocity,
                                        wage_bm_transport,
                                        truck_loading_time,
                                        wage_bm_loading,
                                        OM_hour_MWh,
                                        wage_operation_maintenance)[1]
    row11 = cofiringplant.straw_supply.loading_work(truck_loading_time)[1]
    row12 = cofiringplant.straw_supply.loading_wages(truck_loading_time, wage_bm_loading)[1]

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
                      cofiringplant.straw_supply.transport_time(truck_velocity)
                      )
          )
    print(cols.format('Truck trips: number', cofiringplant.biomass_used[1] / truck_load))
    print()

print_job(MongDuong1, MongDuong1Cofire)

print_job(NinhBinh, NinhBinhCofire)

print('Note: 1 FTE =', FTE)
