# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Job creation assessment of a co-firing project"""

from parameters import winder_capacity, truck_velocity, work_hour_day
from parameters import truck_load, OM_hour_MWh, biomass_ratio, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance

# Note to H: we are working with quantities not numbers
# the results are a "work time" which is a "duration" not a "number of hours".
# M.


def bm_collection_work(cofiringplant):
    """Work time needed to collect straw for co-firing per year"""
    result = cofiringplant.biomass_used[1] * work_hour_day / winder_capacity
    result.display_unit = 'hr'
    return result


# FIXME: Use tkm instead
def bm_transport_work(cofiringplant):
    """Work time needed to transport rice straw to the plant per year"""
    result = number_of_truck_trips(cofiringplant) * transport_time(cofiringplant)
    result.display_unit = 'hr'
    return result


def number_of_truck_trips(cofiringplant):
    """Number of trucks to deliver the required biomass for co-firing to plant"""
    return cofiringplant.biomass_used[1] / truck_load


# FIXME: Trucks don't have to start from the border of the collection zone. Use tkm instead
# FIXME: Trucks load/unload instantly
def transport_time(cofiringplant):
    result = cofiringplant.straw_supply.collection_radius() * 2 / truck_velocity
    result.display_unit = 'hr'
    return result


def om_work(plant):
    """Work time needed for operation and maintenance for co-firing"""
    result = plant.power_generation[0] * biomass_ratio * OM_hour_MWh
    result.display_unit = 'hr'
    return result


def cofiring_work(plant, cofiringplant):
    """Total work time created from co-firing"""
    return bm_collection_work(cofiringplant) + bm_transport_work(cofiringplant) + om_work(plant)


def benefit_bm_collection(cofiringplant):
    """Benefit from job creation from biomass collection"""
    amount = bm_collection_work(cofiringplant) * wage_bm_collect
    amount.display_unit = "kUSD"
    return amount


def benefit_bm_transport(cofiringplant):
    """Benefit from job creation from biomass transportation"""
    amount = bm_transport_work(cofiringplant) * wage_bm_transport
    amount.display_unit = "kUSD"
    return amount


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance"""
    amount = om_work(plant) * wage_operation_maintenance
    amount.display_unit = "kUSD"
    return amount


def total_job_benefit(plant, cofiringplant):
    """Total benefit from job creation from biomass co-firing"""
    return (benefit_bm_collection(cofiringplant)
            + benefit_bm_transport(cofiringplant)
            + benefit_om(plant)
            )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
