# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""The biomass supply chain is a list of zones produing biomass."""

from copy import copy

# pylint: disable=wrong-import-order,too-many-arguments,too-many-instance-attributes
from model.utils import isclose, display_as
from natu.units import t, km, ha


class SupplyZone:
    """A zone from wich biomass is collected.

    Assume that fields are small and everywhere so it has uniform repartition.
    One crop per year is subject to straw collection for sale.
    Only a fraction of the fields are collected and sold, also uniform
    """

    def __init__(self,
                 shape,
                 rice_yield_per_crop,
                 rice_land_fraction,
                 straw_to_rice_ratio,
                 tortuosity_factor,
                 sold_fraction):
        self.shape = shape
        self.rice_yield_per_crop = rice_yield_per_crop
        self.rice_land_fraction = rice_land_fraction
        self.straw_to_rice_ratio = straw_to_rice_ratio
        self.straw_yield_per_crop = rice_yield_per_crop * straw_to_rice_ratio
        self.tortuosity_factor = tortuosity_factor
        self.sold_fraction = sold_fraction

    def __str__(self):
        straw_density = self.straw_yield_per_crop * self.rice_land_fraction
        straw_density = display_as(straw_density, 't/km2')
        return ("Supply zone"
                + "\n Shape: " + str(self.shape)
                + "\n Straw density produced*:   " + str(straw_density)
                + "\n Straw density sold*:       " + str(straw_density * self.sold_fraction)
                + "\n Area:                      " + str(self.area())
                + "\n Rice growing area:         " + str(self.ricegrowing_area())
                + "\n Collected area:            " + str(self.collected_area())
                + "\n Straw available:           " + str(self.straw_available())
                + "\n Straw sold:                " + str(self.straw_sold())
                + "\n Tortuosity:                " + str(self.tortuosity_factor)
                + "\n Activity to transport all: " + str(self.transport_tkm())
                + "\n     Note:  *legacy code"
                + "\n")

    def area(self):
        surface = self.shape.area()
        return display_as(surface, 'ha')

    def ricegrowing_area(self):
        surface = self.area() * self.rice_land_fraction
        return display_as(surface, 'ha')

    def collected_area(self):
        surface = self.ricegrowing_area() * self.sold_fraction
        return display_as(surface, 'ha')

    def straw_available(self):
        mass = self.ricegrowing_area() * self.straw_yield_per_crop
        return display_as(mass, 't')

    def straw_sold(self):
        mass = self.straw_available() * self.sold_fraction
        return display_as(mass, 't')

    def transport_tkm(self):
        activity = (self.straw_yield_per_crop * self.rice_land_fraction * self.sold_fraction
                    * self.shape.first_moment_of_area()
                    * self.tortuosity_factor)
        return display_as(activity, 't * km')

    def shrink(self, factor):
        self.shape = self.shape.shrink(factor)
        return self


class SupplyChain:
    """A collection of supply zones.

    Not vectorized, the supply chain does not vary with time.
    """

    def __init__(self,
                 zones,
                 straw_production,
                 average_straw_yield):
        self.zones = zones
        self.straw_production = straw_production
        self.average_straw_yield = average_straw_yield

    def fit(self, target_quantity):
        """Return a copy of the supply chain adjusted to sell exactly  target_quantity.

        Disgard unused zone(s) and shrink the last one.
        """
        assert target_quantity <= self.straw_sold(), 'Not enough biomass in supply chain: '

        i = 0
        collected = SupplyChain([copy(self.zones[0])],
                                straw_production=self.straw_production,
                                average_straw_yield=self.average_straw_yield)
        while collected.straw_sold() < target_quantity:
            i += 1
            collected.zones.append(copy(self.zones[i]))

        excess = collected.straw_sold() - target_quantity
        assert excess >= 0 * t
        reduction_factor = 1 - excess / collected.zones[i].straw_sold()
        collected.zones[i] = collected.zones[i].shrink(reduction_factor)

        assert isclose(collected.straw_sold(), target_quantity)
        return collected

    def __str__(self):
        result = ("Supply chain\n"
                  + "\nArea:                      " + str(self.area())
                  + "\nRice growing area:         " + str(self.ricegrowing_area())
                  + "\nCollected area:            " + str(self.collected_area())
                  + "\nStraw available:           " + str(self.straw_available())
                  + "\nStraw sold:                " + str(self.straw_sold())
                  + "\nTransport      :           " + str(self.transport_tkm())
                  + "\nCollection_radius:         " + str(self.collection_radius())
                  + "\n")
        for zone in self.zones:
            result += str(zone)
        return result

    def area(self):
        surface = 0 * ha
        for zone in self.zones:
            surface += zone.area()
        return display_as(surface, 'km2')

    def ricegrowing_area(self):
        surface = 0 * ha
        for zone in self.zones:
            surface += zone.ricegrowing_area()
        return display_as(surface, 'km2')

    def collected_area(self):
        surface = 0 * ha
        for zone in self.zones:
            surface += zone.collected_area()
        return display_as(surface, 'km2')

    def straw_available(self):
        mass = 0 * t
        for zone in self.zones:
            mass += zone.straw_available()
        return display_as(mass, 't')

    def straw_sold(self):
        mass = 0 * t
        for zone in self.zones:
            mass += zone.straw_sold()
        return display_as(mass, 't')

    def transport_tkm(self):
        activity = 0 * t * km
        for zone in self.zones:
            activity += zone.transport_tkm()
        return display_as(activity, 't * km')

    def collection_radius(self):
        return self.zones[-1].shape.max_radius()
