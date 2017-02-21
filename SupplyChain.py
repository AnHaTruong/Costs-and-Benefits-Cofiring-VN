# Economic of co-firing in two power plants in Vietnam
#
# A biomass supply chain
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
from units import v_after_invest, as_kUSD, time_step
from natu.units import t, USD
from copy import copy

class SupplyZone():
    def __init__(self, shape, straw_density, transport_tariff, tortuosity_factor):
        self.shape = shape
        self.straw_density = straw_density
        self.transport_tariff = transport_tariff
        self.tortuosity_factor = tortuosity_factor

    def capacity(self):
        return self.shape.area() * self.straw_density

    def transport_cost(self):
        return (self.transport_tariff *
                self.straw_density *
                self.shape.first_moment_of_area() *
                self.tortuosity_factor
                )

    def shrink(self, factor):
        self.shape = self.shape.shrink(factor)
        return self


class SupplyChain():
    def __init__(self, zones):
        self.zones = zones

    def capacity(self):
        total = 0 * t
        for zone in self.zones:
            total += zone.capacity()
        return total

    def transport_all_cost(self):
        cost = 0 * USD
        for zone in self.zones:
            cost += zone.transport_cost()
        cost.display_unit = 'kUSD'
        return cost

    def transport_quantity_cost(self, quantity):
        # quantity.display_unit = 't'
        # print('Quantity transported: ', quantity)
        # print('Chain capacity: ', self.capacity())
        assert quantity <= self.capacity(), 'Not enough biomass in supply chain: '

        i = 0
        collected = SupplyChain([copy(self.zones[0])])   # FIXME: CHANGE A COPY NOT THE ORIGINAL
        while collected.capacity() < quantity:
            i += 1
            collected.zones.append(copy(self.zones[i]))

        excess = collected.capacity() - quantity
        assert excess >= 0 * t
        reduction_factor = excess / collected.zones[i].capacity()
        collected.zones[i] = collected.zones[i].shrink(reduction_factor)

        return collected.transport_all_cost()

    def v_transport_cost(self, biomass_used):
        return v_after_invest * self.transport_quantity_cost(biomass_used[1] * time_step)
