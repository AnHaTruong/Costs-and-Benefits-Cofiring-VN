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
from parameters import wage_bm_collect, wage_operation_maintenance
from biomassrequired import biomass_required
from biomasscost import collection_radius


def bm_collection_work(plant):
    """Total number of hour needed to collect straw for co-firing per year

    >>> from parameters import *
    >>> bm_collection_work(MongDuong1)
    35.991732848796104
    >>> bm_collection_work(NinhBinh)
    7.412339467796653
    """
    return biomass_required(plant) * work_hour_day / winder_capacity


def bm_transport_work(plant):
    """Total number of hour needed to transport rice straw to the plant per year

    >>> from parameters import *
    >>> bm_transport_work(MongDuong1)
    4.6467612441644475
    >>> bm_transport_work(NinhBinh)
    0.21275304488580102
    """
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of trucks to deliver the required biomass for co-firing to plant

    >>> from parameters import *
    >>> print_with_unit(number_of_truck, MongDuong1, '1/y')
    12955.4 1/y
    >>> print_with_unit(number_of_truck, NinhBinh, '1/y')
    2668.1 1/y
    """
    return biomass_required(plant) / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)

    >>> from parameters import *
    >>> print_with_unit(transport_time, MongDuong1, 'hr')
    3.14414 hr
    >>> print_with_unit(transport_time, NinhBinh, 'hr')
    0.698997 hr
    """
    return collection_radius(plant) * 2 / truck_velocity


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
    45.08750162205021
    >>> cofiring_work(NinhBinh)
    8.138439535269724
    """
    return bm_collection_work(plant) + bm_transport_work(plant) + om_work(plant)


def print_with_unit(func, plant, unit):
    l = func(plant)
    l.display_unit = unit
    return l
    

def benefit_bm_collection(plant):
    """Benefit from job creation from biomass collection

    >>> from parameters import *
    >>> print_with_unit(benefit_bm_collection, MongDuong1, 'kUSD/y')
    350.209 kUSD/y
    >>> print_with_unit(benefit_bm_collection, NinhBinh, 'kUSD/y')
    72.124 kUSD/y
    """
    return bm_collection_work(plant) * wage_bm_collect


def benefit_bm_transport(plant):
    """Benefit from job creation from biomass transportation

    >>> from parameters import *
    >>> print_with_unit(benefit_bm_transport, MongDuong1, 'kUSD/y')
    45.2142 kUSD/y
    >>> print_with_unit(benefit_bm_transport, NinhBinh, 'kUSD/y')
    2.07014 kUSD/y
    """
    return bm_transport_work(plant) * wage_bm_transport


def benefit_om(plant):
    """Benefit from job creation from co-firing operation and maintenance

    >>> from parameters import *
    >>> print_with_unit(benefit_om, MongDuong1, 'kUSD/y')
    65.13 kUSD/y
    >>> print_with_unit(benefit_om, NinhBinh, 'kUSD/y')
    7.515 kUSD/y
    """
    return om_work(plant) * wage_operation_maintenance


def total_job_benefit(plant):
    """Total benefit from job creation from biomass co-firing

    >>> from parameters import *
    >>> print_with_unit(total_job_benefit, MongDuong1, 'kUSD/y')
    460.553 kUSD/y
    >>> print_with_unit(total_job_benefit, NinhBinh, 'kUSD/y')
    81.7091 kUSD/y
    """
    return benefit_bm_collection(plant) + benefit_bm_transport(plant) + benefit_om(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
