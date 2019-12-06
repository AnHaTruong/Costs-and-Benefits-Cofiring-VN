# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Represent the collective of resellers."""

from collections import namedtuple

from pandas import Series, DataFrame, set_option

from model.utils import after_invest, display_as

from model.emitter import Emitter, Activity
from model.investment import Investment

ResellerParameter = namedtuple("ResellerParameter",
                               ['barge_fuel_consumption',
                                'truck_loading_time',
                                'wage_bm_loading',
                                'truck_load',
                                'truck_velocity',
                                'fuel_cost_per_hour_driving',
                                'fuel_cost_per_hour_loading',
                                'rental_cost_per_hour',
                                'wage_bm_transport',
                                'time_horizon'])


#pylint: disable=too-many-instance-attributes
class Reseller(Investment, Emitter):
    """The reseller segment of the system.

    Members:
        activity_level:  total  tkm  of transport services provided
        quantity: total mass being transported
        collection_radius: the maximum distance from the plant where biomass is collected

    loading_work and loading_wages proportional to the quantity
    driving_work and driving_wages proportional to the activity level

    emissions are proportional to activity level only (ASSUMPTION)

    The capital is zero, we assume the trucks are rented.
    """

    def __init__(self, supply_chain, transport_parameter, emission_factor):

        Investment.__init__(self, "Reseller", transport_parameter.time_horizon)

        self.parameter = transport_parameter
        self.activity_level = after_invest(supply_chain.transport_tkm(),
                                           self.parameter.time_horizon)
        self.quantity = after_invest(supply_chain.straw_sold(), self.parameter.time_horizon)
        self.collection_radius = supply_chain.collection_radius()

        self.truck_trips = self.quantity / self.parameter.truck_load

        activity = Activity(
            name='Road transport',
            level=self.activity_level,
            emission_factor=emission_factor['road_transport'])
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

    def operating_expenses_detail(self):
        """Tabulate the annual operating expenses."""
        expenses_data = [self.rental_cost(),
                         self.fuel_cost(),
                         self.loading_wages(),
                         self.driving_wages()]
        expenses_index = ['Truck rental',
                          'Truck fuel',
                          'Handling work',
                          'Driving work']
        df = DataFrame(data=expenses_data, index=expenses_index)
        df.loc['= Operating expenses'] = df.sum()
        return df

    def max_trip_time(self):
        time = self.collection_radius / self.parameter.truck_velocity
        return display_as(time, 'hr')

    def parameters_table(self):
        """Tabulate the arguments defining the reseller. Return a Pandas Series."""
        set_option('display.max_colwidth', 80)
        a = Series(self.parameter, self.parameter._fields)
        display_as(a.loc['wage_bm_loading'], "USD / hr")
        display_as(a.loc['fuel_cost_per_hour_driving'], "USD / hr")
        display_as(a.loc['fuel_cost_per_hour_loading'], "USD / hr")
        display_as(a.loc['rental_cost_per_hour'], "USD / hr")
        display_as(a.loc['wage_bm_transport'], "USD / hr")
        display_as(a.loc['barge_fuel_consumption'], "g / t / km")
        return a
