# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Define the class  System  used to instantiate a run of the model."""

import pandas as pd
from natu.numpy import npv

from init import after_invest, year_1, display_as, safe_divide
from powerplant import FuelPowerPlant, CofiringPlant
from farmer import Farmer
from transporter import Transporter


#We should pass the parameters as an object
#pylint: disable=too-many-instance-attributes
class System:
    """The system model of the cofiring economic sector.

    Instance variables: plant, cofiring plant, supply_chain, transporter, farmer.
    The class is designed immutable, don't change the members after initialization.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, plant_parameter, cofire_parameter, supply_chain, price,
                 farm_parameter, transport_parameter):
        """Instantiate the system actors."""
        self.plant = FuelPowerPlant(plant_parameter)
        self.cofiring_plant = CofiringPlant(plant_parameter, cofire_parameter)
        self.supply_chain = supply_chain.fit(self.cofiring_plant.biomass_used[1])
        self.farmer = Farmer(self.supply_chain, farm_parameter)
        self.transporter = Transporter(self.supply_chain, transport_parameter)
        self.price = None
        self.clear_market(price)

    def clear_market(self, price):
        """Realize the payments between actors."""
        self.price = price

        electricity_sales = self.plant.power_generation * price.electricity
        display_as(electricity_sales, 'kUSD')

        self.plant.revenue = electricity_sales
        self.plant.fuel_cost = self.plant.fuel_used * price.coal

        self.cofiring_plant.revenue = electricity_sales
        self.cofiring_plant.fuel_cost = self.cofiring_plant.fuel_used * price.coal

        self.biomass_value = self.cofiring_plant.biomass_used * price.biomass
        display_as(self.biomass_value, "kUSD")

        self.transport_cost = after_invest(self.supply_chain.transport_tkm() * price.transport,
                                           self.transporter.parameter['time_horizon'])
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
        return display_as(self.cofiring_plant.fuel_saved, 't')

    def coal_work_lost(self, mining_productivity):
        time = self.coal_saved / mining_productivity
        return time

    def coal_work_lost_value(self, mining_productivity, mining_wage):
        value = self.coal_work_lost(mining_productivity) * mining_wage
        return display_as(value, 'kUSD')

    def emissions_baseline(self, total=False):
        """Tabulate system annual atmospheric emissions without cofiring."""
        baseline = pd.DataFrame(columns=['CO2', 'NOx', 'PM10', 'SO2'])
        baseline = baseline.append(year_1(self.plant.emissions()))
        baseline = baseline.append(year_1(self.plant.fuel_transporter().emissions()))
        baseline = baseline.append(year_1(self.farmer.emissions_exante))
        if total:
            baseline.loc["Total"] = baseline.sum()
            baseline.loc["Total_plant"] = baseline.iloc[0]
            baseline.loc["Total_transport"] = baseline.iloc[1]
            baseline.loc["Total_field"] = baseline.iloc[2]
        return baseline

    def emissions_cofiring(self, total=False):
        """Tabulate system annual atmospheric emissions with cofiring."""
        cofiring = pd.DataFrame(columns=['CO2', 'NOx', 'PM10', 'SO2'])
        cofiring = cofiring.append(year_1(self.cofiring_plant.emissions()))
        cofiring = cofiring.append(year_1(self.cofiring_plant.fuel_transporter().emissions()))
        cofiring = cofiring.append(year_1(self.farmer.emissions()))
        cofiring = cofiring.append(year_1(self.transporter.emissions()))
        if total:
            cofiring.loc["Total"] = cofiring.sum()
            cofiring.loc["Total_plant"] = cofiring.iloc[0] + cofiring.iloc[1]
            cofiring.loc["Total_transport"] = cofiring.iloc[2] + cofiring.iloc[4]
            cofiring.loc["Total_field"] = cofiring.iloc[3]
        return cofiring

    def emission_reduction(self, external_cost):
        """Tabulate reductions of annual atmospheric emissions with cofiring."""
        plant_reduction = (self.plant.emissions(total=True)['Total']
                           - self.cofiring_plant.emissions(total=True)['Total'])

        transport_reduction = (
            self.plant.fuel_transporter().emissions(total=True)['Total']
            - self.cofiring_plant.fuel_transporter().emissions(total=True)['Total']
            - self.transporter.emissions(total=True)['Total'])

        field_reduction = (self.farmer.emissions_exante['Straw']
                           - self.farmer.emissions(total=True)['Total'])

        total_reduction = plant_reduction + transport_reduction + field_reduction
        total_benefit = total_reduction * external_cost
        total_emission = self.emissions_baseline(total=True).loc["Total"]
        relative_reduction = total_reduction / total_emission
        for pollutant in total_benefit:
            display_as(pollutant, 'kUSD')
        list_of_series = [plant_reduction, transport_reduction, field_reduction,
                          total_reduction, total_benefit, relative_reduction]
        row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit', 'Relative']
        reduction = pd.DataFrame(list_of_series, index=row)
        return reduction

    def mitigation_npv(self, discount_rate, external_cost):
        df = self.emission_reduction(external_cost)
        annual_mitigation_value = df.loc['Benefit', 'CO2']
        value = npv(discount_rate, annual_mitigation_value)
        return display_as(value, 'kUSD')

    def health_npv(self, discount_rate, external_cost):
        df = self.emission_reduction(external_cost)
        annual_health_benefit = df.loc['Benefit'].drop('CO2').sum()
        value = npv(discount_rate, annual_health_benefit)
        return display_as(value, 'kUSD')

    def benefits(self, discount_rate, external_cost):
        """Tabulate the present value of various benefits from co-firing."""
        table = ['']
        table.append(self.cofiring_plant.name)
        table.append('-------------------')
        row2 = '{:30}' + '{:20.0f}'
        table.append(row2.format('Health', self.health_npv(discount_rate, external_cost)))
        table.append(row2.format('Emission reduction',
                                 self.mitigation_npv(discount_rate, external_cost)))
        table.append(row2.format('Wages', self.wages_npv(discount_rate)))
        table.append(row2.format('Farmer earnings before tax',
                                 self.farmer.net_present_value(discount_rate)))
        table.append(row2.format('Trader earnings before tax',
                                 self.transporter.net_present_value(discount_rate)))
        return '\n'.join(table)

    def coal_saved_benefits(self, coal_import_price):
        """Tabulate the quantity and value of coal saved by cofiring."""
        col1 = self.coal_saved[1]
        col2 = display_as(col1 * coal_import_price, 'kUSD')

        row = '{:35}{:23.0f}'
        table = ['Coal saved at ' + str(self.cofiring_plant.name)]
        table.append(row.format('Amount of coal saved from co-firing', col1))
        table.append(row.format('Maximum benefit for trade balance', col2))
        return '\n'.join(table)

    # Code really smell, will change result to DataFrame now.
    # pylint: disable=too-many-locals
    def job_changes(self, mining_parameter):
        """Tabulate the number of full time equivalent (FTE) jobs created/destroyed by cofiring."""
        cols = '{:25}{:12.1f}'
        cols2 = '{:25}{:12.1f}{:12.1f}'

        lines = ['Benefit from job creation: ' + self.plant.name + '\n']

        row7 = self.farmer.labor()[1]
        row1 = self.farmer.labor_cost()[1]
        row8 = self.transporter.driving_work()[1]
        row2 = self.transporter.driving_wages()[1]
        row11 = self.transporter.loading_work()[1]
        row12 = self.transporter.loading_wages()[1]
        row9 = self.cofiring_plant.biomass_om_work()[1]
        row3 = self.cofiring_plant.biomass_om_wages()[1]
        row10 = self.labor[1]
        row4 = self.wages[1]

        display_as(row7, 'FTE')
        display_as(row8, 'FTE')
        display_as(row9, 'FTE')
        display_as(row10, 'FTE')
        display_as(row11, 'FTE')

        lines.append(cols2.format('Biomass collection', row7, row1))
        lines.append(cols2.format('Biomass transportation', row8, row2))
        lines.append(cols2.format('Biomass loading', row11, row12))
        lines.append(cols2.format('O&M', row9, row3))
        lines.append(cols2.format('Total', row10, row4))
        lines.append('')
        lines.append(cols.format('Area collected', self.supply_chain.area()))
        lines.append(cols.format('Collection radius', self.supply_chain.collection_radius()))
        lines.append(cols.format('Maximum transport time', self.transporter.max_trip_time()))
        lines.append(cols.format('Number of truck trips', self.transporter.truck_trips[1]))
        lines.append('')
        lines.append('Mining job lost from co-firing at ' + self.plant.name + '\n')
        row = self.coal_work_lost(mining_parameter['productivity_underground'])[1]
        display_as(row, 'FTE')
        lines.append(cols.format('Job lost', row))
        lines.append(cols.format('Coal saved', self.coal_saved[1]))
        return '\n'.join(lines)
