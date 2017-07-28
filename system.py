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
from powerplant import PowerPlant, CofiringPlant
from farmer import Farmer
from transporter import Transporter


class System:
    """The system model of the cofiring economic sector.

    Members: plant, cofiring plant, supply_chain, transporter, farmer
    The cofiring plant pays the farmer for biomass and the transporter for transport
    """

    # pylint: disable=too-many-arguments
    def __init__(self, plant_parameter, cofire_parameter, supply_chain, price,
                 farm_parameter, transport_parameter):

        self.plant = PowerPlant(plant_parameter)
        self.cofiring_plant = CofiringPlant(plant_parameter, cofire_parameter)
        self.supply_chain = supply_chain.fit(self.cofiring_plant.biomass_used[1])
        self.farmer = Farmer(self.supply_chain, farm_parameter)
        self.transporter = Transporter(self.supply_chain, transport_parameter)

        electricity_sales = self.plant.power_generation * price.electricity
        display_as(electricity_sales, 'kUSD')
        self.plant.revenue = electricity_sales
        self.cofiring_plant.coal_cost = self.cofiring_plant.coal_used * price.coal

        self.plant.coal_cost = self.plant.coal_used * price.coal
        self.cofiring_plant.revenue = electricity_sales

        self.biomass_value = self.cofiring_plant.biomass_used * price.biomass
        display_as(self.biomass_value, "kUSD")

        self.transport_cost = self.supply_chain.transport_tkm() * price.transport
        display_as(self.transport_cost, "kUSD")

        self.cofiring_plant.biomass_cost = self.biomass_value + self.transport_cost
        self.farmer.revenue = self.biomass_value
        self.transporter.revenue = self.transport_cost

    @property
    def transport_cost_per_t(self):
        return safe_divide(self.transport_cost, self.cofiring_plant.biomass_used)

    @property
    def labor(self):
        """Return total work time created from co-firing."""
        time = (self.farmer.labor()
                + self.transporter.labor()
                + self.cofiring_plant.biomass_om_work())
        return display_as(time, 'hr')

    @property
    def wages(self):
        """Return total benefit from job creation from biomass co-firing."""
        amount = (self.farmer.labor_cost()
                  + self.transporter.labor_cost()
                  + self.cofiring_plant.biomass_om_wages())
        return display_as(amount, 'kUSD')

    def wages_npv(self, discount_rate):
        amount = npv(discount_rate, self.wages)
        return display_as(amount, 'kUSD')

    @property
    def coal_saved(self):
        return display_as(self.cofiring_plant.coal_saved, 't')

    def coal_work_lost(self, mining_productivity):
        time = self.coal_saved / mining_productivity
        return time

    def emission_reduction(self, external_cost):
        plant_reduction = (self.plant.emissions()['Total']
                           - self.cofiring_plant.emissions()['Total'])

        transport_reduction = (self.plant.coal_transporter().emissions()['Total']
                               - self.cofiring_plant.coal_transporter().emissions()['Total']
                               - self.transporter.emissions()['Total'])

        field_reduction = (self.farmer.emissions_exante['Total']
                           - self.farmer.emissions()['Total'])

        total_reduction = plant_reduction + transport_reduction + field_reduction
        total_benefit = total_reduction * external_cost
        for pollutant in total_benefit:
            display_as(pollutant, 'kUSD')
        list_of_series = [plant_reduction, transport_reduction, field_reduction,
                          total_reduction, total_benefit]
        row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
        reduction = pd.DataFrame(list_of_series, index=row)
        return reduction

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
