# Economic of co-firing in two power plants in Vietnam
#
# A biomass supply chain
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
from units import isclose
from natu.units import t, km, USD
from copy import copy


class SupplyZone():
    def __init__(self, shape, straw_density, transport_tariff, tortuosity_factor):
        self.shape = shape
        self.straw_density = straw_density
        self.straw_density.display_unit = 't/km2'
        self.transport_tariff = transport_tariff
        self.transport_tariff.display_unit = 'USD/(t*km)'
        self.tortuosity_factor = tortuosity_factor

    def __str__(self):
        return ("Supply zone" +
                "\n Shape: " + str(self.shape) +
                "\n Straw density: " + str(self.straw_density) +
                "\n Capacity = " + str(self.capacity()) +
                "\n Transport tariff: " + str(self.transport_tariff) +
                "\n Tortuosity: " + str(self.tortuosity_factor) +
                "\n Activity to transport all = " + str(self.transport_tkm()) +
                "\n Cost to transport all = " + str(self.transport_cost())
                )

    def capacity(self):
        mass = self.shape.area() * self.straw_density
        mass.display_unit = 't'
        return mass

    def transport_tkm(self):
        activity = self.straw_density * self.shape.first_moment_of_area() * self.tortuosity_factor
        activity.display_unit = 't*km'
        return activity

    def transport_cost(self):
        cost = self.transport_tariff * self.transport_tkm()
        cost.display_unit = 'kUSD'
        return cost

    def shrink(self, factor):
        self.shape = self.shape.shrink(factor)
        return self


class SupplyChain():
    def __init__(self, zones):
        self.zones = zones

    def __str__(self):
        s = "Supply chain\n"
        s += "Capacity = " + str(self.capacity()) + "\n"
        s += "Cost to transport all = " + str(self.transport_cost()) + "\n"
        s += "Collection_radius = " + str(self.collection_radius()) + "\n"
        for zone in self.zones:
            s += str(zone) + "\n"
        return s

    def capacity(self):
        mass = 0 * t
        for zone in self.zones:
            mass += zone.capacity()
        mass.display_unit = 't'
        return mass

    def transport_tkm(self):
        activity = 0 * t * km
        for zone in self.zones:
            activity += zone.transport_tkm()
        activity.display_unit = 't * km'
        return activity

    def transport_cost(self):
        cost = 0 * USD
        for zone in self.zones:
            cost += zone.transport_cost()
        cost.display_unit = 'kUSD'
        return cost

    def fit(self, quantity):
        """Returns an new supply chain, disgard unused zone(s) and shrink the last one"""
        assert quantity <= self.capacity(), 'Not enough biomass in supply chain: '

        i = 0
        collected = SupplyChain([copy(self.zones[0])])
        while collected.capacity() < quantity:
            i += 1
            collected.zones.append(copy(self.zones[i]))

        excess = collected.capacity() - quantity
        assert excess >= 0 * t
        reduction_factor = 1 - excess / collected.zones[i].capacity()
        collected.zones[i] = collected.zones[i].shrink(reduction_factor)

        #        quantity.display_unit = 't'
        #        print('Quantity transported: ', quantity, '\n')
        #        print('Initial ', self)
        #        print('Excess = ', excess)
        #        print('Reduction factor = ', reduction_factor)
        #        print('')
        #        print('Collected ', collected)

        assert isclose(collected.capacity(), quantity)
        return collected

    def collection_radius(self):
        return self.zones[-1].shape.outer_radius()
