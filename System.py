# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

import pandas as pd
from natu.numpy import npv, errstate

from init import display_as
from PowerPlant import CofiringPlant
from Farmer import Farmer
from Transporter import Transporter

#FIXME: The transport cost is not accounted.
#TODO:  The transporter is a trader. He buys the straw from the farmers, transport it and resell.
#       There are two prices.


class System:
    """The model

    Has a plant, cofiring plant, supply_chain, transporter, farmer
    Do the financial transaction
    """
    def __init__(self, plant, cofire_tech, supply_chain,
                 biomass_price, emission_factor, collect_economics, truck_economics):
        self.plant = plant
        self.cofiring_plant = CofiringPlant(plant, cofire_tech)

        self.biomass_used = self.cofiring_plant.biomass_used

        self.supply_chain = supply_chain.fit(self.biomass_used[1])

        self.farmer = Farmer(self.supply_chain, emission_factor, collect_economics)

        self.transporter = Transporter(self.supply_chain, emission_factor, truck_economics)

        self.biomass_value = self.biomass_used * biomass_price
        display_as(self.biomass_value, "kUSD")

        self.transport_cost = self.transporter.activity_level * truck_economics["transport_tariff"]
        display_as(self.transport_cost, "kUSD")

        self.cofiring_plant.biomass_cost = self.biomass_value + self.transport_cost
        self.farmer.revenue = self.biomass_value + self.transport_cost

    def transport_cost_per_t(self):
        with errstate(divide='ignore', invalid='ignore'):
            cost_per_t = self.transport_cost / self.biomass_used
        return display_as(cost_per_t, 'USD/t')

    def labor(self):
        """Total work time created from co-firing"""
        time = (self.farmer.labor()
                + self.transporter.labor()
                + self.cofiring_plant.biomass_om_work())
        return display_as(time, 'hr')

    def wages(self):
        """Total benefit from job creation from biomass co-firing"""
        amount = (self.farmer.labor_cost()
                  + self.transporter.labor_cost()
                  + self.cofiring_plant.biomass_om_wages())
        return display_as(amount, 'kUSD')

    def wages_npv(self, discount_rate):
        amount = npv(discount_rate, self.wages())
        return display_as(amount, 'kUSD')

    # TODO: Keep this method quantities only, leave economic valuation to CO2_npv and health_npv.
    def emission_reduction(self, external_cost):
        plant_ER = (self.plant.stack.emissions()['Total']
                    - self.cofiring_plant.stack.emissions()['Total'])
        transport_ER = (self.plant.coal_transporter().emissions()['Total']
                        - self.cofiring_plant.coal_transporter().emissions()['Total']
                        - self.transporter.emissions()['Total'])
        field_ER = (self.farmer.emissions_exante['Total']
                    - self.farmer.emissions()['Total'])
        total_ER = plant_ER + transport_ER + field_ER
        # Over the model time horizon, non discounted... better drop it
        total_benefit = total_ER * external_cost
        for pollutant in total_benefit:
            display_as(pollutant, 'kUSD')
        list_of_series = [plant_ER, transport_ER, field_ER, total_ER, total_benefit]
        row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
        ER_table = pd.DataFrame(list_of_series, index=row)
        return ER_table

    def CO2_npv(self, discount_rate, external_cost):
        df = self.emission_reduction(external_cost)
        v = df.loc['Benefit', 'CO2']
        value = npv(discount_rate, v)
        return display_as(value, 'kUSD')

    def health_npv(self, discount_rate, external_cost):
        df = self.emission_reduction(external_cost)
        v = df.loc['Benefit'].drop('CO2').sum()
        value = npv(discount_rate, v)
        return display_as(value, 'kUSD')
