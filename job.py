# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Job creation assessment of a co-firing project"""

from parameters import winder_capacity, work_hour_day, truck_velocity
from parameters import truck_load, OM_hour_MWh, biomass_ratio


def bm_collection_work(plant):
    """Total number of hour needed to collect straw for co-firing per year"""
    return plant.biomass_required * work_hour_day / winder_capacity


def bm_transport_work(plant):
    """Total number of hour needed to transport rice straw to the plant per year"""
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of trucks to deliver the required biomass for co-firing to plant
    """
    return plant.biomass_required / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)"""
    return plant.collection_radius * 2 / truck_velocity


def om_work(plant):
    """Total number of hour needed for operation and maintenance for co-firing
    """
    return plant.generation * biomass_ratio * OM_hour_MWh


def cofiring_work(plant):
    """Total number of hours created from co-firing"""
    return bm_collection_work(plant) + bm_transport_work(plant) + om_work(plant)
