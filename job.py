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

from parameters import winder_capacity, truck_velocity, work_hour_day
from parameters import truck_load, OM_hour_MWh, biomass_ratio, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance
from biomassrequired import biomass_required


def bm_collection_work(plant):
    """Total number of hour needed to collect straw for co-firing per year
    """
    return biomass_required(plant) * work_hour_day / winder_capacity


# FIXME: Use tkm instead
def bm_transport_work(cofiringplant):
    """Total number of hour needed to transport rice straw to the plant per year
    """
    return number_of_truck(cofiringplant) * transport_time(cofiringplant)


def number_of_truck(cofiringplant):
    """Number of trucks to deliver the required biomass for co-firing to plant
    """
    return cofiringplant.biomass_used[1] / truck_load


# FIXME: Trucks don't have to start from the border of the collection zone. Use tkm instead
def transport_time(cofiringplant):
    return cofiringplant.active_chain.collection_radius() * 2 / truck_velocity


def om_work(plant):
    """Total number of hour needed for operation and maintenance for co-firing
    """
    return plant.power_generation[0] * biomass_ratio * OM_hour_MWh


def cofiring_work(plant, cofiringplant):
    """Total number of hours created from co-firing
    """
    return bm_collection_work(plant) + bm_transport_work(cofiringplant) + om_work(plant)


def benefit_bm_collection(plant):
    """Benefit from job creation from biomass collection
    """
    return bm_collection_work(plant) * wage_bm_collect


def benefit_bm_transport(cofiringplant):
    """Benefit from job creation from biomass transportation
    """
    return bm_transport_work(cofiringplant) * wage_bm_transport


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance
    """
    return om_work(plant) * wage_operation_maintenance


def total_job_benefit(plant, cofiringplant):
    """Total benefit from job creation from biomass co-firing
    """
    return benefit_bm_collection(plant) + benefit_bm_transport(cofiringplant) + benefit_om(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
