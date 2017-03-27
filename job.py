# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Job creation assessment of a co-firing project

Approximation "Small biomass ratio"
We don't count the lower O&M work for the coal firing parts of the plant.

Approximation "Substitutes imported coal"
We don't count the jobs destroyed in the coal mining sector.
"""
# TODO: Put the global  OM_hour_MWh  in proper scope
from init import display_as

from parameters import winder_haul, truck_velocity, work_hour_day, truck_loading_time
from parameters import truck_load, OM_hour_MWh, biomass_ratio, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance, wage_bm_loading


def number_of_truck_trips(cofiringplant):
    """Number of trucks to deliver the required biomass for co-firing to plant"""
    return cofiringplant.biomass_used[1] / truck_load


def transport_time(cofiringplant):
    time = cofiringplant.straw_supply.collection_radius() * 2 / truck_velocity
    return display_as(time, 'hr')


def bm_collection_work(cofiringplant):
    """Work time needed to collect straw for co-firing per year"""
    time = cofiringplant.biomass_used[1] * work_hour_day / winder_haul
    return display_as(time, 'hr')


def bm_transport_work(cofiringplant):
    time = cofiringplant.straw_supply.transport_tkm() / truck_load / truck_velocity
    return display_as(time, 'hr')


def bm_loading_work(cofiringplant):  # Unloading work is included in om_work
    time = cofiringplant.biomass_used[1] * truck_loading_time
    return display_as(time, 'hr')


def om_work(plant):
    """Work time needed for operation and maintenance for co-firing"""
    time = plant.power_generation[0] * biomass_ratio * OM_hour_MWh
    return display_as(time, 'hr')


def cofiring_work(plant, cofiringplant):
    """Total work time created from co-firing"""
    time = (bm_collection_work(cofiringplant) +
            bm_transport_work(cofiringplant)[1] +
            om_work(plant) +
            bm_loading_work(cofiringplant))
    return display_as(time, 'hr')


def benefit_bm_collection(cofiringplant):
    """Benefit from job creation from biomass collection"""
    amount = bm_collection_work(cofiringplant) * wage_bm_collect
    return display_as(amount, 'kUSD')


def benefit_bm_transport(cofiringplant):
    """Benefit from job creation from biomass transportation"""
    amount = bm_transport_work(cofiringplant) * wage_bm_transport
    return display_as(amount, 'kUSD')


def benefit_bm_loading(cofiringplant):
    amount = bm_loading_work(cofiringplant) * wage_bm_loading
    return display_as(amount, 'kUSD')


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance"""
    amount = om_work(plant) * wage_operation_maintenance
    return display_as(amount, 'kUSD')


def total_job_benefit(plant, cofiringplant):
    """Total benefit from job creation from biomass co-firing"""
    return (benefit_bm_collection(cofiringplant)
            + benefit_bm_transport(cofiringplant)[1]
            + benefit_om(plant)
            + benefit_bm_loading(cofiringplant)
            )
