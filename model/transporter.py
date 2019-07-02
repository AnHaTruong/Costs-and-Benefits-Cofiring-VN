# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Represent the collective of transporters."""

from collections import namedtuple

import pandas as pd

from model.utils import after_invest, display_as, USD, kUSD

from model.emitter import Emitter, Activity
from model.investment import Investment

TransporterParameter = namedtuple("TransporterParameter",
                                  ['barge_fuel_consumption',
                                   'truck_loading_time',
                                   'wage_bm_loading',
                                   'truck_load',
                                   'truck_velocity',
                                   'fuel_cost_per_hour_driving',
                                   'fuel_cost_per_hour_loading',
                                   'rental_cost_per_hour',
                                   'wage_bm_transport',
                                   'emission_factor',
                                   'time_horizon'])


#pylint: disable=too-many-instance-attributes
class Transporter(Investment, Emitter):
    """The transporter segment of the system.

    Members:
        activity_level:  total  tkm  of transport services provided
        quantity: total mass being transported
        collection_radius: the maximum distance from the plant where biomass is collected

    loading_work and loading_wages proportional to the quantity
    driving_work and driving_wages proportional to the activity level

    emissions are proportional to activity level only (ASSUMPTION)

    The capital is zero, we assume the trucks are rented.
    """

    def __init__(self, supply_chain, transport_parameter):

        Investment.__init__(self, "Transporter", transport_parameter.time_horizon)

        self.parameter = transport_parameter
        self.activity_level = after_invest(supply_chain.transport_tkm(),
                                           self.parameter.time_horizon)
        self.quantity = after_invest(supply_chain.quantity_sold(), self.parameter.time_horizon)
        self.collection_radius = supply_chain.collection_radius()

        self.truck_trips = self.quantity / self.parameter.truck_load

        activity = Activity(
            name='Road transport',
            level=self.activity_level,
            emission_factor=self.parameter.emission_factor['road_transport'])
        Emitter.__init__(self, activity)

    def loading_work(self):  # Unloading work is included in om_work
        time = self.quantity * self.parameter.truck_loading_time
        return display_as(time, 'hr')

    def driving_work(self):
        time = self.activity_level / self.parameter.truck_load / self.parameter.truck_velocity
        return display_as(time, 'hr')

    def labor(self):
        time = self.loading_work() + self.driving_work()
        return display_as(time, 'hr')

    def loading_wages(self):
        amount = self.loading_work() * self.parameter.wage_bm_loading
        return display_as(amount, 'kUSD')

    def driving_wages(self):
        amount = self.driving_work() * self.parameter.wage_bm_transport
        return display_as(amount, 'kUSD')

    def labor_cost(self):
        amount = self.loading_wages() + self.driving_wages()
        return display_as(amount, 'kUSD')

    def fuel_cost(self):
        amount = (self.driving_work() * self.parameter.fuel_cost_per_hour_driving
                  + self.loading_work() * self.parameter.fuel_cost_per_hour_loading)
        return display_as(amount, 'kUSD')

    def rental_cost(self):
        amount = self.labor() * self.parameter.rental_cost_per_hour
        return display_as(amount, 'kUSD')

    def operating_expenses(self):
        amount = self.labor_cost() + self.fuel_cost() + self.rental_cost()
        return display_as(amount, 'kUSD')

    def max_trip_time(self):
        time = self.collection_radius / self.parameter.truck_velocity
        return display_as(time, 'hr')

    def earning_before_tax_detail(self):
        """Tabulate the annual net income before taxes in the transporting segment."""
        self.expenses = [self.costs_of_goods_sold[1],
                         self.rental_cost()[1],
                         self.fuel_cost()[1],
                         self.loading_wages()[1],
                         self.driving_wages()[1]]
        self.expenses_index = ['- Buying straw',
                               '- Truck rental',
                               '- Truck fuel',
                               '- Handling work',
                               '- Driving work']

        df = Investment.earning_before_tax_detail(self)

        per_trip = df / self.truck_trips[1] * kUSD / USD
        per_trip.columns = ['USD/trip']

        return pd.concat([df, per_trip], axis=1)
