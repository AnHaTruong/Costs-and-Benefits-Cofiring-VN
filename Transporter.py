# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Transporter: """

from init import display_as, USD

from Emitter import Emitter
from Investment import Investment


class Transporter(Investment, Emitter):
    """Represents the collective of transporters

    quantity: total mass being transported
    activity_level:  total  tkm  of transport services provided, determines driving cost and work

    loading_work and loading_wages proportional to the quantity
    driving_work and driving_wages proportional to the activity level
    """
    def __init__(self, supply_chain, emission_factor, transport_parameter):

        Investment.__init__(self)
        self.activity_level = supply_chain.transport_tkm()
        Emitter.__init__(self, {'Road transport': self.activity_level}, emission_factor)

        self.quantity = supply_chain.quantity()
        self.collection_radius = supply_chain.collection_radius()

        self.parameter = transport_parameter
        self.truck_load = self.parameter['truck_load']
        self.truck_trips = self.quantity / self.truck_load

    def loading_work(self):  # Unloading work is included in om_work
        time = self.quantity * self.parameter['truck_loading_time']
        return display_as(time, 'hr')

    def driving_work(self):
        time = self.activity_level / self.truck_load / self.parameter['truck_velocity']
        return display_as(time, 'hr')

    def labor(self):
        time = self.loading_work() + self.driving_work()
        return display_as(time, 'hr')

    def loading_wages(self):
        amount = self.loading_work() * self.parameter['wage_bm_loading']
        return display_as(amount, 'kUSD')

    def driving_wages(self):
        amount = self.driving_work() * self.parameter['wage_bm_transport']
        return display_as(amount, 'kUSD')

    def labor_cost(self):
        amount = self.loading_wages() + self.driving_wages()
        return display_as(amount, 'kUSD')

    def fuel_cost(self):
        amount = 0 * USD
        return display_as(amount, 'kUSD')

    def capital_cost(self):
        amount = 0 * USD
        return display_as(amount, 'kUSD')

    def operating_expenses(self):
        amount = self.labor_cost() + self.fuel_cost() + self.capital_cost()
        return display_as(amount, 'kUSD')

    def max_trip_time(self):
        time = self.collection_radius / self.parameter['truck_velocity']
        return display_as(time, 'hr')
