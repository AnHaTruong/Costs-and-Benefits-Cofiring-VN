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

from parameters import winder_capacity, work_hour_day, FTE, truck_velocity
from parameters import truck_load, OM_hour_MWh, biomass_ratio, time_step


def FTE_bm_collection(plant):
    """Number of job created from rice straw collection"""
    return hour_bm_collection(plant) / FTE

def hour_bm_collection(plant):
    """Total number of hour needed to collect straw for co-firing per year"""
    return plant.biomass_required * work_hour_day / winder_capacity


def FTE_bm_transport(plant):
    """Number of job created from rice straw transportation"""
    return hour_bm_transport(plant) / FTE


def hour_bm_transport(plant):
    """Total number of hour needed to transport rice straw to the plant per year"""
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of truck to deliver the required biomass for co-firing to plant
    """
    return plant.biomass_required / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)"""
    return plant.collection_radius * 2 / truck_velocity

def FTE_OM(plant):
    """Number of job created from operation and maintenance for co-firing
    """
    return hour_om(plant) / FTE


def hour_om(plant):
    """Total number of hour needed for operation and maintenance for co-firing
    """
    return plant.generation * biomass_ratio * OM_hour_MWh


def total_FTE(plant):
    """Total number of job created from co-firing"""
    return FTE_bm_collection(plant) + FTE_bm_transport(plant) + FTE_OM(plant)
