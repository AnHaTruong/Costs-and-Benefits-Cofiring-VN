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
from parameters import truck_load, OM_hour_MWh, biomass_ratio, wage_bm_transport
from parameters import wage_bm_collect, wage_operation_maintenance, h_per_yr


def bm_collection_work(plant):
    """Total number of hour needed to collect straw for co-firing per year

    >>> from parameters import *
    >>> bm_collection_work(MongDuong1)
    35.991732848796104
    >>> bm_collection_work(NinhBinh)
    7.412339467796658
    """
    return plant.biomass_required * work_hour_day / winder_capacity


def bm_transport_work(plant):
    """Total number of hour needed to transport rice straw to the plant per year

    >>> from parameters import *
    >>> bm_transport_work(MongDuong1)
    4.646758278363899
    >>> bm_transport_work(NinhBinh)
    0.21275279613165468
    """
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of trucks to deliver the required biomass for co-firing to plant

    >>> from parameters import *
    >>> number_of_truck(MongDuong1)
    12955.4 1/y
    >>> number_of_truck(NinhBinh)
    2668.1 1/y
    """
    return plant.biomass_required / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)

    >>> from parameters import *
    >>> transport_time(MongDuong1)
    3.14414 hr
    >>> transport_time(NinhBinh)
    0.698996 hr
    """
    return plant.collection_radius * 2 / truck_velocity


def om_work(plant):
    """Total number of hour needed for operation and maintenance for co-firing

    >>> from parameters import *
    >>> om_work(MongDuong1)
    4.449007529089665
    >>> om_work(NinhBinh)
    0.5133470225872689
    """
    return plant.generation * biomass_ratio * OM_hour_MWh


def cofiring_work(plant):
    """Total number of hours created from co-firing


    >>> from parameters import *
    >>> cofiring_work(MongDuong1)
    45.087498656249664
    >>> cofiring_work(NinhBinh)
    8.138439286515581
    """
    return bm_collection_work(plant) + bm_transport_work(plant) + om_work(plant)


def benefit_bm_collection(plant):
    """Benefit from job creation from biomass collection

    >>> from parameters import *
    >>> l = benefit_bm_collection(MongDuong1)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    350.209 kUSD/y
    >>> l = benefit_bm_collection(NinhBinh)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    72.124 kUSD/y
    """
    return bm_collection_work(plant) * wage_bm_collect


def benefit_bm_transport(plant):
    """Benefit from job creation from biomass transportation

    >>> from parameters import *
    >>> l = benefit_bm_transport(MongDuong1)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    45.2142 kUSD/y
    >>> l = benefit_bm_transport(NinhBinh)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    2.07014 kUSD/y
    """
    return bm_transport_work(plant) * wage_bm_transport


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance

    >>> from parameters import *
    >>> l = benefit_om(MongDuong1)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    65.13 kUSD/y
    >>> l = benefit_om(NinhBinh)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    7.515 kUSD/y
    """
    return om_work(plant) * wage_operation_maintenance


def total_job_benefit(plant):
    """Total benefit from job creation from biomass co-firing

    >>> from parameters import *
    >>> l = total_job_benefit(MongDuong1)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    460.553 kUSD/y
    >>> l = total_job_benefit(NinhBinh)
    >>> l.display_unit = 'kUSD/y'
    >>> l
    81.7091 kUSD/y
    """
    return benefit_bm_collection(plant) + benefit_bm_transport(plant) + benefit_om(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
