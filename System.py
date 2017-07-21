# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

import pandas as pd
from natu.numpy import npv

from init import display_as, zero_to_NaN
from PowerPlant import CofiringPlant
from Farmer import Farmer
from Transporter import Transporter

#FIXME: The transport cost is not accounted.
#TODO:  The transporter is a trader. He buys the straw from the farmers, transport it and resell.
#       There are two prices.


class System:
    """
    """
    def __init__(self, plant, cofire_tech, supply_chain,
                 straw_price, emission_factor, collect_economics, truck_economics):
        self.cofiring_plant = CofiringPlant(plant, cofire_tech, straw_price)

        self.biomass_used = self.cofiring_plant.biomass_used

        self.supply_chain = supply_chain.fit(self.biomass_used[1])

        self.farmer = Farmer(self.supply_chain, emission_factor, collect_economics, straw_price)

        self.transporter = Transporter(self.supply_chain, emission_factor, truck_economics)

        # Farmer sells the straw to the plant
        self.contract_value = self.farmer.straw_value() + self.supply_chain.transport_cost()
        self.cofiring_plant.straw_cost = self.contract_value
        self.farmer.income = self.contract_value

    def sourcing_cost(self):
        cost = self.farmer.income() + self.transport.income()
        return display_as(cost, 'kUSD')

    def sourcing_cost_per_t(self):
        """Including transport cost"""
        cost_per_t = self.sourcing_cost() / zero_to_NaN(self.biomass_used)
        return display_as(cost_per_t, 'USD/t')

    def sourcing_cost_per_GJ(self, heat_value):
        cost = self.sourcing_cost_per_t() / heat_value
        return display_as(cost, 'USD / GJ')

    def labor(self):
        """Total work time created from co-firing"""
        time = (self.farmer.labor()
                + self.transporter.labor()
                + self.cofiring_plant.biomass_om_work())
        return display_as(time, 'hr')

    def wages(self):
        """Total benefit from job creation from biomass co-firing"""
        amount = (self.farmer.labor_costs()
                  + self.transporter.labor_cost()
                  + self.cofiring_plant.biomass_om_wages())
        return display_as(amount, 'kUSD')

    def wages_npv(self, discount_rate):
        amount = npv(discount_rate, self.wages())
        return display_as(amount, 'kUSD')

    def emission_reduction(self, specific_cost):
        plant_ER = (self.plant.stack.emissions()['Total']
                    - self.stack.emissions()['Total'])
        transport_ER = (self.plant.coal_transporter().emissions()['Total']
                        - self.coal_transporter().emissions()['Total']
                        - self.straw_supply.transport_emissions()['Total'])
        field_ER = (self.straw_supply.field_emission(self.biomass_used * 0)['Total']
                    - self.straw_supply.field_emission(self.biomass_used)['Total'])
        total_ER = plant_ER + transport_ER + field_ER
        total_benefit = total_ER * specific_cost
        for pollutant in total_benefit:
            display_as(pollutant, 'kUSD')
        list_of_series = [plant_ER, transport_ER, field_ER, total_ER, total_benefit]
        row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
        ER_table = pd.DataFrame(list_of_series, index=row)
        return ER_table

    def CO2_npv(self, discount_rate, specific_cost):
        df = self.emission_reduction(specific_cost)
        v = df['CO2']['Benefit']  # FIXME: use .loc
        value = npv(discount_rate, v)
        return display_as(value, 'kUSD')

    def health_npv(self, discount_rate, specific_cost):
        df = self.emission_reduction(specific_cost)
        v = df.ix['Benefit'].drop('CO2').sum()
        value = npv(discount_rate, v)
        return display_as(value, 'kUSD')
