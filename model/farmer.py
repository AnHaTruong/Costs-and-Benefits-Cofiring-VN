# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Represent the collective of farmers producing biomass."""

import pandas as pd
import numpy as np

from natu.units import ha

from utils import after_invest, display_as, USD, kUSD
from emitter import Emitter, Activity
from investment import Investment


class Farmer(Investment, Emitter):
    """The farming segment of the system: farmers who produce and sell straw.

    As an Investment, the Farmer.revenue has to be set after initialization.
    The capital is zero, we assume the winder is rented.
    """

    def __init__(self, supply_chain, farmer_parameter):
        self.parameter = farmer_parameter
        self.quantity = after_invest(supply_chain.quantity(), self.parameter['time_horizon'])
        self.farm_area = after_invest(supply_chain.quantity() / supply_chain.average_straw_yield,
                                      self.parameter['time_horizon'])

        field_burning_before = Activity(
            name='Straw',
            level=np.ones(self.parameter['time_horizon'] + 1) * supply_chain.burnable(),
            emission_factor=self.parameter['emission_factor']['straw'])

        self.emissions_exante = Emitter(field_burning_before).emissions(total=False)

        field_burning = Activity(
            name='Straw',
            level=field_burning_before.level - self.quantity,
            emission_factor=self.parameter['emission_factor']['straw'])

        winder_use = Activity(
            name='diesel',
            level=self.quantity / (self.parameter['winder_haul'] / self.parameter['fuel_use']),
            emission_factor=self.parameter['emission_factor']['diesel'])

        Emitter.__init__(self, field_burning, winder_use)

        Investment.__init__(self, "Farmers", self.parameter['time_horizon'])

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

    def rental_cost(self):
        amount = self.farm_area * self.parameter['winder_rental_cost']
        return display_as(amount, 'kUSD')

    def operating_expenses(self):
        expenses = self.labor_cost() + self.rental_cost() + self.fuel_cost()
        return display_as(expenses, 'kUSD')

    def earning_before_tax_detail(self):
        """Tabulate the annual net income before taxes in the farming segment."""
        self.expenses = [self.rental_cost()[1], self.fuel_cost()[1], self.labor_cost()[1]]
        self.expenses_index = ['- Winder rental', '- Winder fuel', '- Collection work']
        df = Investment.earning_before_tax_detail(self)

        per_ha = df / (self.farm_area[1] / ha) * kUSD / USD
        per_ha.columns = ['USD/ha']

        return pd.concat([df, per_ha], axis=1)
