# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""The biomass supply chain is a list of zones produing biomass."""

from copy import copy

from init import isclose, AFTER_INVEST, ZEROS, display_as

from natu.units import t, km, ha


class SupplyZone:
    """A zone from wich biomass is collected.

    Members: shape, straw_density, tortuosity factor
    """

    def __init__(self,
                 shape,
                 straw_density,
                 tortuosity_factor):
        self.shape = shape
        self.straw_density = display_as(straw_density, 't/km2')
        self.tortuosity_factor = tortuosity_factor

    def __str__(self):
        return ("Supply zone"
                + "\n Shape: " + str(self.shape)
                + "\n Straw density: " + str(self.straw_density)
                + "\n quantity = " + str(self.quantity())
                + "\n Tortuosity: " + str(self.tortuosity_factor)
                + "\n Activity to transport all = " + str(self.transport_tkm()[1])
                )

    def area(self):
        a = self.shape.area()
        return display_as(a, 'ha')

    def quantity(self):
        mass = AFTER_INVEST * self.shape.area() * self.straw_density
        return display_as(mass, 't')

    def transport_tkm(self):
        activity = (AFTER_INVEST
                    * self.straw_density
                    * self.shape.first_moment_of_area()
                    * self.tortuosity_factor
                    )
        return display_as(activity, 't * km')

    def shrink(self, factor):
        self.shape = self.shape.shrink(factor)
        return self


class SupplyChain:
    """A collection of supply zones.

    Not vectorized, the supply chain does not vary with time
    """

    def __init__(self,
                 zones,
                 straw_production,
                 straw_burn_rate,
                 average_straw_yield):
        self.zones = zones
        self.straw_production = straw_production
        self.straw_burn_rate = straw_burn_rate
        self.average_straw_yield = average_straw_yield

    def fit(self, target_quantity):
        """Return a copy of the supply chain adjusted to produce exactly  target_quantity.

        Disgard unused zone(s) and shrink the last one.
        """
        assert target_quantity <= self.quantity()[1], 'Not enough biomass in supply chain: '

        i = 0
        collected = SupplyChain([copy(self.zones[0])],
                                straw_production=self.straw_production,
                                straw_burn_rate=self.straw_burn_rate,
                                average_straw_yield=self.average_straw_yield)
        while collected.quantity()[1] < target_quantity:
            i += 1
            collected.zones.append(copy(self.zones[i]))

        excess = collected.quantity()[1] - target_quantity
        assert excess >= 0 * t
        reduction_factor = 1 - excess / collected.zones[i].quantity()[1]
        collected.zones[i] = collected.zones[i].shrink(reduction_factor)

        assert isclose(collected.quantity()[1], target_quantity)
        return collected

    def __str__(self):
        s = "Supply chain\n"
        s += "quantity = " + str(self.quantity()) + "\n"
        s += "Collection_radius = " + str(self.collection_radius()) + "\n"
        for zone in self.zones:
            s += str(zone) + "\n"
        return s

    def area(self):
        a = 0 * ha
        for zone in self.zones:
            a += zone.area()
        return display_as(a, 'km2')

    def quantity(self):
        mass = ZEROS * t
        for zone in self.zones:
            mass += zone.quantity()
        return display_as(mass, 't')

    def transport_tkm(self):
        activity = ZEROS * t * km
        for zone in self.zones:
            activity += zone.transport_tkm()
        return display_as(activity, 't * km')

    def collection_radius(self):
        return self.zones[-1].shape.outer_radius()

    def burnable(self):
        mass = self.straw_production * self.straw_burn_rate
        return display_as(mass, 't')
