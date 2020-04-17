# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Represent the collective of farmers producing biomass."""

from collections import namedtuple

from pandas import Series, DataFrame, set_option

from model.utils import t, after_invest_new, display_as, ONES

from model.emitter import Emitter, Activity
from model.investment import Investment


FarmerParameter = namedtuple(
    "FarmerParameter",
    [
        "winder_rental_cost",
        "winder_haul",
        "work_hour_day",
        "wage_bm_collect",
        "fuel_cost_per_hour",
        "open_burn_rate",
        "fuel_use",
    ],
)


class Farmer(Investment, Emitter):
    """The farming segment of the system: farmers who produce and sell straw.

    As an Investment, the Farmer.revenue has to be set after initialization.
    The capital is zero, we assume the winder is rented.
    """

    def __init__(self, supply_chain, farmer_parameter, emission_factor):
        self.parameter = farmer_parameter
        self.emission_factor = emission_factor
        self.quantity = after_invest_new(supply_chain.straw_sold())

        self.winder_use_area = after_invest_new(supply_chain.collected_area())

        # ex-ante baseline emissions are one crop, in the supply zone
        straw_burned = (
            supply_chain.straw_available() * farmer_parameter.open_burn_rate / t
        )

        field_burning_before = Activity(
            name="Straw",
            level=ONES * straw_burned * t,
            emission_factor=self.emission_factor["straw_open"],
        )

        self.emissions_exante = Emitter(field_burning_before).emissions(total=False)

        # We assume that all biomass collected would have been burned in open field.
        assert all(
            field_burning_before.level >= self.quantity
        ), "Not enough biomass open burned."
        field_burning = Activity(
            name="Straw",
            level=field_burning_before.level - self.quantity,
            emission_factor=self.emission_factor["straw_open"],
        )

        winder_use = Activity(
            name="diesel",
            level=self.quantity
            / (self.parameter.winder_haul / self.parameter.fuel_use),
            emission_factor=self.emission_factor["diesel"],
        )

        Emitter.__init__(self, field_burning, winder_use)

        Investment.__init__(self, "Farmers")

    def labor(self):
        """Work time needed to collect straw for co-firing per year."""
        t_per_hr = self.parameter.winder_haul / self.parameter.work_hour_day
        time = self.quantity / t_per_hr
        return display_as(time, "hr")

    def labor_cost(self):
        """Benefit from job creation from biomass collection."""
        amount = self.labor() * self.parameter.wage_bm_collect
        return display_as(amount, "kUSD")

    def fuel_cost(self):
        amount = self.labor() * self.parameter.fuel_cost_per_hour
        return display_as(amount, "kUSD")

    def rental_cost(self):
        amount = self.winder_use_area * self.parameter.winder_rental_cost
        return display_as(amount, "kUSD")

    def operating_expenses(self):
        expenses = self.labor_cost() + self.rental_cost() + self.fuel_cost()
        return display_as(expenses, "kUSD")

    def operating_expenses_detail(self):
        """Return a DataFrame with years in column and annual operating expenses in row."""
        expenses_data = [self.rental_cost(), self.fuel_cost(), self.labor_cost()]
        expenses_index = ["Winder rental", "Winder fuel", "Collection work"]
        df = DataFrame(data=expenses_data, index=expenses_index)
        df.loc["= Operating expenses"] = df.sum()
        return df

    def parameters_table(self):
        """Tabulate the arguments defining the farmer. Return a Pandas Series."""
        set_option("display.max_colwidth", 80)
        a = Series(self.parameter, self.parameter._fields)
        display_as(a.loc["winder_rental_cost"], "USD / ha")
        display_as(a.loc["wage_bm_collect"], "USD / hr")
        display_as(a.loc["fuel_cost_per_hour"], "USD / hr")
        return a
