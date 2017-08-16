# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Represent the collective of transporters."""

import pandas as pd

from init import after_invest, display_as, USD

from emitter import Emitter, Activity
from investment import Investment


class Transporter(Investment, Emitter):
    """The collective of transporters.

    Members:
        activity_level:  total  tkm  of transport services provided
        quantity: total mass being transported
        collection_radius: the maximum distance from the plant where biomass is collected

    loading_work and loading_wages proportional to the quantity
    driving_work and driving_wages proportional to the activity level

    emissions are proportional to activity level only (ASSUMPTION)
    """

    def __init__(self, supply_chain, transport_parameter):

        Investment.__init__(self)

        self.activity_level = after_invest(supply_chain.transport_tkm())
        self.quantity = after_invest(supply_chain.quantity())
        self.collection_radius = supply_chain.collection_radius()

        self.parameter = transport_parameter
        self.truck_load = self.parameter['truck_load']
        self.truck_trips = self.quantity / self.truck_load

        activity = Activity(
            name='Road transport',
            level=self.activity_level,
            emission_factor=self.parameter['emission_factor']['road_transport'])
        Emitter.__init__(self, activity)

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
        amount = (self.driving_work() * self.parameter['fuel_cost_per_hour_driving']
                  + self.loading_work() * self.parameter['fuel_cost_per_hour_loading'])
        return display_as(amount, 'kUSD')

    def capital_cost(self):
        amount = self.labor() * self.parameter['capital_cost_per_hour']
        return display_as(amount, 'kUSD')

    def operating_expenses(self):
        amount = self.labor_cost()   # + self.fuel_cost() + self.capital_cost()
        return display_as(amount, 'kUSD')

    def max_trip_time(self):
        time = self.collection_radius / self.parameter['truck_velocity']
        return display_as(time, 'hr')

    def income_statement(self):
        """Summarize the economic implications of transporting acticity."""
        headings = ['Transport revenue',
                    '- Truck rental',
                    '- Truck fuel',
                    '- Handling work',
                    '- Driving work']

        cash_flows = pd.Series(
            data=[self.revenue[1],
                  - self.capital_cost()[1],
                  - self.fuel_cost()[1],
                  - self.loading_wages()[1],
                  - self.driving_wages()[1]],
            index=headings)

        df = pd.DataFrame(
            data=[cash_flows / (1000 * USD),
                  cash_flows / self.truck_trips[1] / USD],
            index=["Total", "Per_trip"])
        df["= Net income"] = df.sum(axis=1)
        df["Unit"] = ['kUSD', 'USD']
        return df[["Unit"] + headings + ["= Net income"]].T
