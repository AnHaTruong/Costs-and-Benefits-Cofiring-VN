# encoding: utf-8
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
    def __init__(self,
                 shape,
                 straw_density,
                 transport_tariff,
                 tortuosity_factor):
        self.shape = shape
        self.straw_density = display_as(straw_density, 't/km2')
        self.transport_tariff = display_as(transport_tariff, 'USD/(t*km)')
        self.tortuosity_factor = tortuosity_factor

    def __str__(self):
        return ("Supply zone" +
                "\n Shape: " + str(self.shape) +
                "\n Straw density: " + str(self.straw_density) +
                "\n quantity = " + str(self.quantity()) +
                "\n Transport tariff: " + str(self.transport_tariff) +
                "\n Tortuosity: " + str(self.tortuosity_factor) +
                "\n Activity to transport all = " + str(self.transport_tkm()[1]) +
                "\n Cost to transport all = " + str(self.transport_cost()[1])
                )

    def area(self):
        a = self.shape.area()
        return display_as(a, 'ha')

    def quantity(self):
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
    def __init__(self,
                 zones,
                 straw_production,
                 straw_burn_rate,
                 average_straw_yield,
                 emission_factor):
        self.zones = zones
        self.straw_production = straw_production
        self.straw_burn_rate = straw_burn_rate
        self.average_straw_yield = average_straw_yield
        self.emission_factor = emission_factor

    def fit(self, target_quantity):
        """Returns a copy of the supply chain
           which is adjusted to produce exactly  target_quantity
           disgard unused zone(s) and shrink the last one"""
        assert target_quantity <= self.quantity()[1], 'Not enough biomass in supply chain: '

        i = 0
        collected = SupplyChain([copy(self.zones[0])],
                                straw_production=self.straw_production,
                                straw_burn_rate=self.straw_burn_rate,
                                average_straw_yield=self.average_straw_yield,
                                emission_factor=self.emission_factor)
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

    def quantity(self):
        mass = v_zeros * t
        for zone in self.zones:
            mass += zone.quantity()
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
        cost_per_t = self.transport_cost() / zero_to_NaN(self.quantity())
        return display_as(cost_per_t, 'USD/t')

    def field_cost(self, price):
        cost = self.quantity() * price
        return display_as(cost, 'kUSD')

    def cost(self, price):
        cost = self.field_cost(price) + self.transport_cost()
        return display_as(cost, 'kUSD')

    def cost_per_t(self, price):
        """Including transport cost"""
        cost_per_t = self.cost(price) / zero_to_NaN(self.quantity())
        return display_as(cost_per_t, 'USD/t')

    def cost_per_GJ(self, price, heat_value):
        cost = self.cost_per_t(price) / heat_value
        return display_as(cost, 'USD / GJ')

    def collection_radius(self):
        return self.zones[-1].shape.outer_radius()

    def field_emission(self, biomass_used):
        field = Emitter({'Straw': (v_after_invest * self.straw_production *
                                   self.straw_burn_rate) - biomass_used},
                        self.emission_factor
                        )
        return field.emissions()

    def farm_revenue_per_ha(self, straw_price):
        revenue = self.average_straw_yield * straw_price
        return display_as(revenue, 'USD/ha')

    def farm_income_per_ha(self, winder_rental_cost, straw_price):
        income = self.farm_revenue_per_ha(straw_price) - winder_rental_cost
        return display_as(income, 'USD/ha')

    def farm_area(self):
        area = self.quantity() / self.average_straw_yield
        return display_as(area, 'ha')

    def farm_income(self, winder_rental_cost, straw_price):
        """ Total benefit for the farmers from having extra income selling
            rice straw to the plant for co-firing
            """
        income = (self.farm_area()
                * self.farm_income_per_ha(winder_rental_cost, straw_price))
        return display_as(income, 'kUSD')