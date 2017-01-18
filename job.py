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

from unitsdef import time_step
from parameters import winder_capacity, truck_velocity, work_hour_day
from parameters import truck_load, OM_hour_MWh, biomass_ratio, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance
from biomassrequired import biomass_required
from biomasscost import collection_radius


def print_with_unit(func, plant, unit):
    """ Display the desired unit on Tables"""
    value = func(plant)
    value.display_unit = unit
    return value


def bm_collection_work(plant):
    """Total number of hour needed to collect straw for co-firing per year

    >>> from parameters import *
    >>> bm_collection_work(MongDuong1)
    31.453275005976963
    >>> bm_collection_work(NinhBinh)
    5.5446671167748685
    """
    return biomass_required(plant) * work_hour_day / winder_capacity


def bm_transport_work(plant):
    """Total number of hour needed to transport rice straw to the plant per year

    >>> from parameters import *
    >>> bm_transport_work(MongDuong1)
    3.918564866790392
    >>> bm_transport_work(NinhBinh)
    0.1376436085135254
    """
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of trucks to deliver the required biomass for co-firing to plant

    >>> from parameters import *
    >>> print_with_unit(number_of_truck, MongDuong1, '1/y')
    11321.7 1/y
    >>> print_with_unit(number_of_truck, NinhBinh, '1/y')
    1995.82 1/y
    """
    return biomass_required(plant) / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)

    >>> from parameters import *
    >>> print_with_unit(transport_time, MongDuong1, 'hr')
    3.034 hr
    >>> print_with_unit(transport_time, NinhBinh, 'hr')
    0.604554 hr
    """
    return collection_radius(plant) * 2 / truck_velocity


def om_work(plant):
    """Total number of hour needed for operation and maintenance for co-firing

    >>> from parameters import *
    >>> om_work(MongDuong1)
    3.888
    >>> om_work(NinhBinh)
    0.38400000000000006
    """
    return plant.power_generation * biomass_ratio * OM_hour_MWh / time_step


def cofiring_work(plant):
    """Total number of hours created from co-firing

    >>> from parameters import *
    >>> cofiring_work(MongDuong1)
    39.25983987276735
    >>> cofiring_work(NinhBinh)
    6.066310725288394
    """
    return bm_collection_work(plant) + bm_transport_work(plant) + om_work(plant)


def benefit_bm_collection(plant):
    """Benefit from job creation from biomass collection

    >>> from parameters import *
    >>> print_with_unit(benefit_bm_collection, MongDuong1, 'kUSD/y')
    306.049 kUSD/y
    >>> print_with_unit(benefit_bm_collection, NinhBinh, 'kUSD/y')
    53.9511 kUSD/y
    """
    return bm_collection_work(plant) * wage_bm_collect


def benefit_bm_transport(plant):
    """Benefit from job creation from biomass transportation

    >>> from parameters import *
    >>> print_with_unit(benefit_bm_transport, MongDuong1, 'kUSD/y')
    38.1287 kUSD/y
    >>> print_with_unit(benefit_bm_transport, NinhBinh, 'kUSD/y')
    1.33931 kUSD/y
    """
    return bm_transport_work(plant) * wage_bm_transport


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance

    >>> from parameters import *
    >>> print_with_unit(benefit_om, MongDuong1, 'kUSD/y')
    56.9173 kUSD/y
    >>> print_with_unit(benefit_om, NinhBinh, 'kUSD/y')
    5.62146 kUSD/y
    """
    return om_work(plant) * wage_operation_maintenance


def total_job_benefit(plant):
    """Total benefit from job creation from biomass co-firing

    >>> from parameters import *
    >>> print_with_unit(total_job_benefit, MongDuong1, 'kUSD/y')
    401.094 kUSD/y
    >>> print_with_unit(total_job_benefit, NinhBinh, 'kUSD/y')
    60.9118 kUSD/y
    """
    return benefit_bm_collection(plant) + benefit_bm_transport(plant) + benefit_om(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
