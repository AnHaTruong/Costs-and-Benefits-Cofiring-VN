# Economic of co-firing in two power plants in Vietnam
#
# A biomass supply chain
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
# pylint: disable=E0611

from copy import copy
from init import isclose, v_after_invest, v_zeros, display_as, zero_to_NaN, USD

from natu.units import t, km, ha
from Emitter import Emitter


class SupplyZone():
    def __init__(self, shape, straw_density, transport_tariff, tortuosity_factor):
        self.shape = shape
        self.straw_density = display_as(straw_density, 't/km2')
        self.transport_tariff = display_as(transport_tariff, 'USD/(t*km)')
        self.tortuosity_factor = tortuosity_factor

    def __str__(self):
        return ("Supply zone" +
                "\n Shape: " + str(self.shape) +
                "\n Straw density: " + str(self.straw_density) +
                "\n tonnage = " + str(self.tonnage()) +
                "\n Transport tariff: " + str(self.transport_tariff) +
                "\n Tortuosity: " + str(self.tortuosity_factor) +
                "\n Activity to transport all = " + str(self.transport_tkm()[1]) +
                "\n Cost to transport all = " + str(self.transport_cost()[1])
                )

    def area(self):
        a = self.shape.area()
        return display_as(a, 'ha')

    def tonnage(self):
        mass = v_after_invest * self.shape.area() * self.straw_density
        return display_as(mass, 't')

    def transport_tkm(self):
        activity = (v_after_invest
                    * self.straw_density
                    * self.shape.first_moment_of_area()
                    * self.tortuosity_factor
                    )
        return display_as(activity, 't * km')

    def transport_cost(self):
        cost = self.transport_tkm() * self.transport_tariff
        return display_as(cost, 'kUSD')

    def shrink(self, factor):
        self.shape = self.shape.shrink(factor)
        return self


class SupplyChain():
    """A collection of supply zones
    - The supply chain does not vary with time
    """
    def __init__(self, zones, emission_factor):
        self.zones = zones
        self.emission_factor = emission_factor

    def __str__(self):
        s = "Supply chain\n"
        s += "tonnage = " + str(self.tonnage()) + "\n"
        s += "Cost to transport all = " + str(self.transport_cost()[1]) + "\n"
        s += "Collection_radius = " + str(self.collection_radius()) + "\n"
        for zone in self.zones:
            s += str(zone) + "\n"
        return s

    def area(self):
        a = 0 * ha
        for zone in self.zones:
            a += zone.area()
        return display_as(a, 'km2')

    def tonnage(self):
        mass = v_zeros * t
        for zone in self.zones:
            mass += zone.tonnage()
        return display_as(mass, 't')

    def transport_tkm(self):
        activity = v_zeros * t * km
        for zone in self.zones:
            activity += zone.transport_tkm()
        return display_as(activity, 't * km')

    def transport_cost(self):
        cost = v_zeros * USD
        for zone in self.zones:
            cost += zone.transport_cost()
        return display_as(cost, 'kUSD')

    def transport_emissions(self):
        trucks = Emitter({'Road transport': self.transport_tkm()},
                         self.emission_factor)
        return trucks.emissions()

    def transport_cost_per_t(self):
        cost_per_t = self.transport_cost() / zero_to_NaN(self.tonnage())
        return display_as(cost_per_t, 'USD/t')

    def field_cost(self, price):
        cost = self.tonnage() * price
        return display_as(cost, 'kUSD')

    def cost(self, price):
        cost = self.field_cost(price) + self.transport_cost()
        return display_as(cost, 'kUSD')

    def cost_per_t(self, price):
        """Including transport cost"""
        cost_per_t = self.cost(price) / zero_to_NaN(self.tonnage())
        return display_as(cost_per_t, 'USD/t')

    def cost_per_GJ(self, price, heat_value):
        cost = self.cost_per_t(price) / heat_value
        return display_as(cost, 'USD / GJ')

    def fit(self, quantity):
        """Returns an new supply chain, disgard unused zone(s) and shrink the last one"""
        assert quantity <= self.tonnage()[1], 'Not enough biomass in supply chain: '

        i = 0
        collected = SupplyChain([copy(self.zones[0])], emission_factor=self.emission_factor)
        while collected.tonnage()[1] < quantity:
            i += 1
            collected.zones.append(copy(self.zones[i]))

        excess = collected.tonnage()[1] - quantity
        assert excess >= 0 * t
        reduction_factor = 1 - excess / collected.zones[i].tonnage()[1]
        collected.zones[i] = collected.zones[i].shrink(reduction_factor)

        assert isclose(collected.tonnage()[1], quantity)
        return collected

    def collection_radius(self):
        return self.zones[-1].shape.outer_radius()
