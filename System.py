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

from init import display_as, safe_divide
from PowerPlant import CofiringPlant
from Farmer import Farmer
from Transporter import Transporter


class System:
    """The cofiring sector and its market

    Has a plant, cofiring plant, supply_chain, transporter, farmer
    The cofiring plant pays the farmer for biomass and the transporter for transport
    """
    def __init__(self, plant, cofire_tech, feedin_tariff,
                 supply_chain, biomass_price, emission_factor, collect_economics, truck_economics):
        self.plant = plant
        self.cofiring_plant = CofiringPlant(plant, cofire_tech)
        self.supply_chain = supply_chain.fit(self.cofiring_plant.biomass_used[1])
        self.farmer = Farmer(self.supply_chain, emission_factor, collect_economics)
        self.transporter = Transporter(self.supply_chain, emission_factor, truck_economics)

        electricity_sales = plant.power_generation * feedin_tariff
        display_as(electricity_sales, 'kUSD')
        self.plant.revenue = electricity_sales
        self.cofiring_plant.revenue = electricity_sales

        self.biomass_value = self.cofiring_plant.biomass_used * biomass_price
        display_as(self.biomass_value, "kUSD")

        self.transport_cost = self.transporter.activity_level * truck_economics["transport_tariff"]
        display_as(self.transport_cost, "kUSD")

        self.cofiring_plant.biomass_cost = self.biomass_value + self.transport_cost
        self.farmer.revenue = self.biomass_value
        self.transporter.revenue = self.transport_cost

    def transport_cost_per_t(self):
        return safe_divide(self.transport_cost, self.cofiring_plant.biomass_used)

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

    def emission_reduction(self, external_cost):
        plant_ER = (self.plant.emissions()['Total']
                    - self.cofiring_plant.emissions()['Total'])
        transport_ER = (self.plant.coal_transporter().emissions()['Total']
                        - self.cofiring_plant.coal_transporter().emissions()['Total']
                        - self.transporter.emissions()['Total'])
        field_ER = (self.farmer.emissions_exante['Total']
                    - self.farmer.emissions()['Total'])
        total_ER = plant_ER + transport_ER + field_ER
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
