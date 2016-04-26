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
    """Total number of hour needed to collect straw for co-firing per year

    >>> from parameters import *
    >>> bm_collection_work(MongDuong1)
    <Quantity(315503.5301525467, 'hour / year')>
    >>> bm_collection_work(NinhBinh)
    <Quantity(64976.56777470551, 'hour / year')>
    """
    return plant.biomass_required * work_hour_day / winder_capacity


def bm_transport_work(plant):
    """Total number of hour needed to transport rice straw to the plant per year

    >>> from parameters import *
    >>> bm_transport_work(MongDuong1)
    <Quantity(40733.483068137946, 'hour / year')>
    >>> bm_transport_work(NinhBinh)
    <Quantity(1864.991010890085, 'hour / year')>
    """
    return number_of_truck(plant) * transport_time(plant)


def number_of_truck(plant):
    """Number of trucks to deliver the required biomass for co-firing to plant

    >>> from parameters import *
    >>> number_of_truck(MongDuong1)
    <Quantity(12955.36370688895, '1 / year')>
    >>> number_of_truck(NinhBinh)
    <Quantity(2668.1003142488453, '1 / year')>
    """
    return plant.biomass_required / truck_load


def transport_time(plant):
    """Time for 1 truck to deliver biomass to the plant (round trip)

    >>> from parameters import *
    >>> transport_time(MongDuong1)
    <Quantity(3.1441404494478316, 'hour')>
    >>> transport_time(NinhBinh)
    <Quantity(0.6989958364497022, 'hour')>
    """
    return plant.collection_radius * 2 / truck_velocity


def om_work(plant):
    """Total number of hour needed for operation and maintenance for co-firing

    >>> from parameters import *
    >>> om_work(MongDuong1)
    <Quantity(39.0, 'gigawatt_hour * hour / megawatt_hour / year')>
    >>> om_work(NinhBinh)
    <Quantity(4.5, 'gigawatt_hour * hour / megawatt_hour / year')>
    """
    return plant.generation * biomass_ratio * OM_hour_MWh


def cofiring_work(plant):
    """Total number of hours created from co-firing


    >>> from parameters import *
    >>> cofiring_work(MongDuong1)
    <Quantity(395237.01322068466, 'hour / year')>
    >>> cofiring_work(NinhBinh)
    <Quantity(71341.5587855956, 'hour / year')>
    """
    return bm_collection_work(plant) + bm_transport_work(plant) + om_work(plant)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
