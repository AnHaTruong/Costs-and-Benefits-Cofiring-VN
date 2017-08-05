# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Represent the collective of farmers producing biomass."""

import pandas as pd

from natu.units import ha

from init import AFTER_INVEST, ONES, display_as, USD
from emitter import Emitter, Activity
from investment import Investment


class Farmer(Investment, Emitter):
    """The collective of farmers who produce and sell straw.

    As an Investment, the Farmer.revenue has to be set after initialization.
    """

    def __init__(self, supply_chain, farmer_parameter):
        self.quantity = supply_chain.quantity()
        self.parameter = farmer_parameter
        self.farm_area = self.quantity / supply_chain.average_straw_yield

        field_burning_before = Activity(
            name='Straw',
            level=ONES * supply_chain.burnable(),
            emission_factor=self.parameter['emission_factor']['straw'])

        self.emissions_exante = Emitter(field_burning_before).emissions()

        field_burning = Activity(
            name='Straw',
            level=field_burning_before.level - AFTER_INVEST * self.quantity,
            emission_factor=self.parameter['emission_factor']['straw'])

        Emitter.__init__(self, field_burning)

        Investment.__init__(self)

    def labor(self):
        """Work time needed to collect straw for co-firing per year."""
        t_per_hr = self.parameter['winder_haul'] / self.parameter['work_hour_day']
        time = self.quantity / t_per_hr
        return display_as(time, 'hr')

    def labor_cost(self):
        """Benefit from job creation from biomass collection."""
        amount = self.labor() * self.parameter['wage_bm_collect']
        return display_as(amount, 'kUSD')

    def fuel_cost(self):
        amount = self.labor() * self.parameter['fuel_cost_per_hour']
        return display_as(amount, 'kUSD')

    def capital_cost(self):
        amount = self.farm_area * self.parameter['winder_rental_cost']
        return display_as(amount, 'kUSD')

    def operating_expenses(self):
        expenses = self.labor_cost() + self.capital_cost() + self.fuel_cost()
        return display_as(expenses, 'kUSD')

    def income_statement(self):
        """Summarize the economic implications of collecting and selling straw."""
        headings = ['Straw revenue',
                    '- Winder rental',
                    '- Winder fuel',
                    '- Collection work']

        cash_flows = pd.Series(
            data=[self.revenue[1],
                  - self.capital_cost()[1],
                  - self.fuel_cost()[1],
                  - self.labor_cost()[1]],
            index=headings)

        df = pd.DataFrame(
            data=[cash_flows / (1000 * USD),
                  cash_flows / self.farm_area[1] / (USD / ha)],
            index=["Total",
                   "Per ha"])
        df["= Net income"] = df.sum(axis=1)
        df["Unit"] = ['kUSD', 'USD/ha']
        return df[["Unit"] + headings + ["= Net income"]].T
