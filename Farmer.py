# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

from init import v_after_invest, v_ones, display_as
from Emitter import Emitter
from Investment import Investment


class Farmer(Investment, Emitter):
    """Farmer class represents the collective of farmers who produce and sell straw
    """
    def __init__(self,
                 supply_chain,
                 emission_factor,
                 collect_economics):
        self.quantity = supply_chain.quantity()
        self.collect_economics = collect_economics
        self.farm_area = self.quantity / supply_chain.average_straw_yield
        self.capital_cost = self.collect_economics['winder_rental_cost'] * self.farm_area[1]

        field_burned_exante = v_ones * supply_chain.burnable()
        self.emissions_exante = Emitter({'Straw': field_burned_exante},
                                        emission_factor).emissions()

        field_burned = field_burned_exante - v_after_invest * self.quantity
        Emitter.__init__(self, {'Straw': field_burned}, emission_factor)

        Investment.__init__(self)

    def labor(self):
        """Work time needed to collect straw for co-firing per year"""
        time = (self.quantity
                * self. collect_economics['work_hour_day']
                / self.collect_economics['winder_haul'])
        return display_as(time, 'hr')

    def labor_cost(self):
        """Benefit from job creation from biomass collection"""
        amount = self.labor() * self.collect_economics['wage_bm_collect']
        return display_as(amount, 'kUSD')

    def operating_expenses(self):
        expenses = self.labor_cost() + self.capital_cost
        return display_as(expenses, 'kUSD')
