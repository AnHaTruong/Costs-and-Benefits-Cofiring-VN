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

from units import time_step
from parameters import winder_capacity, truck_velocity, work_hour_day
from parameters import truck_load, OM_hour_MWh, biomass_ratio, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance
from biomassrequired import biomass_required
from biomasscost import collection_radius
from units import print_with_unit


def bm_collection_work(plant):
    """Total number of hour needed to collect straw for co-firing per year
    """
    return biomass_required(plant) * work_hour_day / winder_capacity


def bm_transport_work(plant):
    """Total number of hour needed to transport rice straw to the plant per year
    """
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of trucks to deliver the required biomass for co-firing to plant
    """
    return biomass_required(plant) / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)
    """
    return collection_radius(plant) * 2 / truck_velocity


def om_work(plant):
    """Total number of hour needed for operation and maintenance for co-firing
    """
    return plant.power_generation * biomass_ratio * OM_hour_MWh


def cofiring_work(plant):
    """Total number of hours created from co-firing
    """
    return bm_collection_work(plant) + bm_transport_work(plant) + om_work(plant)


def benefit_bm_collection(plant):
    """Benefit from job creation from biomass collection
    """
    return bm_collection_work(plant) * wage_bm_collect


def benefit_bm_transport(plant):
    """Benefit from job creation from biomass transportation
    """
    return bm_transport_work(plant) * wage_bm_transport


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance
    """
    return om_work(plant) * wage_operation_maintenance


def total_job_benefit(plant):
    """Total benefit from job creation from biomass co-firing
    """
    return benefit_bm_collection(plant) + benefit_bm_transport(plant) + benefit_om(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
