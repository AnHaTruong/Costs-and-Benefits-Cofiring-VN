# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A Power plant
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
# pylint: disable=E0611

import pandas as pd
from natu.numpy import full, npv

from init import time_horizon, v_after_invest, display_as, USD
from Investment import Investment
from Emitter import Fuel, Emitter


class PowerPlant(Investment):
    """ A coal power plant, without co-firing"""
    def __init__(self,
                 name: str,
                 capacity,
                 capacity_factor,    # Must be net of self consumption
                 commissioning: int,
                 boiler_technology: str,
                 plant_efficiency,
                 boiler_efficiency,
                 fix_om_coal,
                 variable_om_coal,
                 emission_controls,
                 emission_factor,
                 coal: Fuel,
                 capital=0 * USD
                 ):
        self.name = name
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.plant_efficiency = plant_efficiency
        self.boiler_efficiency = boiler_efficiency
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
        self.emission_controls = emission_controls
        self.emission_factor = emission_factor
        self.coal = coal
        super().__init__(capital)

        self.power_generation = full(time_horizon + 1,
                                     capacity * capacity_factor,
                                     dtype=object)
        display_as(self.power_generation, 'GWh')

        self.gross_heat_input = self.power_generation / plant_efficiency
        display_as(self.gross_heat_input, 'TJ')

        self.coal_used = self.gross_heat_input / coal.heat_value
        display_as(self.coal_used, 't')

        self.stack = Emitter({self.coal.name: self.coal_used},
                             self.emission_factor,
                             self.emission_controls)

    def income(self, feedin_tariff):
        revenue = self.power_generation * feedin_tariff
        return display_as(revenue, 'kUSD')

    def operating_expenses(self):
        cost = self.fuel_cost() + self.operation_maintenance_cost()
        return display_as(cost, 'kUSD')

    def coal_cost(self):
        cost = self.coal_used * self.coal.price
        return display_as(cost, 'kUSD')

    def coal_transport_tkm(self):
        return self.coal_used * 2 * self.coal.transport_distance   # Return trip inputed

    def coal_transporter(self):
        return Emitter({self.coal.transport_mean: self.coal_transport_tkm()},
                       self.emission_factor
                       )

    def fuel_cost(self):
        return self.coal_cost()

    def coal_om_cost(self):
        fixed_om_coal = full(time_horizon + 1,
                             self.fix_om_coal * self.capacity,
                             dtype=object)
        variable_om_coal = self.power_generation * self.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        return display_as(self.coal_om_cost(), 'kUSD')

    def lcoe(self, feedin_tariff, discount_rate, tax_rate, depreciation_period):
        total_lifetime_power_production = npv(discount_rate, self.power_generation)
        total_life_cycle_cost = npv(discount_rate,
                                    self.cash_out(feedin_tariff,
                                                  tax_rate,
                                                  depreciation_period))
        result = total_life_cycle_cost / total_lifetime_power_production
        # Fixme: once TableC is no regression, use /MWh for integer
        return display_as(result, 'USD/kWh')

    def table_LCOE(self, feedin_tariff, discount_rate, tax_rate, depreciation_period):
        def printRowInt(label, quantity):
            print('{:30}{:8.0f}'.format(label, quantity))

        def printRowFloat(label, value):
            print('{:30}{:8.4f}'.format(label, value))

        def printRowNPV(label, vector):
            printRowInt(label, npv(discount_rate, vector))

        print("Levelized cost of electricity -", self.name, "\n")
        printRowInt("Investment", self.capital)
        printRowNPV("Fuel cost", self.fuel_cost())
        printRowNPV("O&M cost", self.operation_maintenance_cost())
        printRowNPV("Tax", self.income_tax(feedin_tariff, tax_rate, depreciation_period))
        printRowNPV("Sum of costs", self.cash_out(feedin_tariff,
                                                  tax_rate,
                                                  depreciation_period))
        printRowNPV("Electricity produced", self.power_generation)
        printRowFloat("LCOE", self.lcoe(feedin_tariff,
                                        discount_rate,
                                        tax_rate,
                                        depreciation_period))
        print('')


class CofiringPlant(PowerPlant):

    def __init__(self,
                 plant: PowerPlant,
                 biomass_ratio,
                 capital_cost,
                 fix_om_cost,
                 variable_om_cost,
                 biomass: Fuel,
                 boiler_efficiency_loss,
                 supply_chain
                 ):

        self.plant = plant
        self.biomass_ratio = biomass_ratio
        self.capital_cost = capital_cost
        self.fix_om_cost = fix_om_cost
        self.variable_om_cost = variable_om_cost
        self.biomass = biomass

        biomass_ratio_mass = biomass_ratio * (plant.coal.heat_value / biomass.heat_value)

        cofiring_boiler_efficiency = (plant.boiler_efficiency
                                      - boiler_efficiency_loss(biomass_ratio_mass))
        cofiring_boiler_efficiency[0] = plant.boiler_efficiency[0]

        cofiring_plant_efficiency = (plant.plant_efficiency
                                     * cofiring_boiler_efficiency / plant.boiler_efficiency)
        cofiring_plant_efficiency[0] = plant.plant_efficiency[0]

        super().__init__(
            plant.name + " Cofire",
            plant.capacity,
            plant.capacity_factor,
            plant.commissioning,
            plant.boiler_technology,
            cofiring_plant_efficiency,
            cofiring_boiler_efficiency,
            plant.fix_om_coal,
            plant.variable_om_coal,
            plant.emission_controls,
            plant.emission_factor,
            plant.coal,
            capital_cost * plant.capacity * float(biomass_ratio[1]))

        self.biomass_heat = v_after_invest * self.gross_heat_input * biomass_ratio
        display_as(self.biomass_heat, 'TJ')

        self.biomass_used = self.biomass_heat / biomass.heat_value
        display_as(self.biomass_used, 't')

        self.coal_saved = self.biomass_heat / plant.coal.heat_value
        display_as(self.coal_saved, 't')

        self.coal_used = (self.gross_heat_input - self.biomass_heat) / self.coal.heat_value
        display_as(self.coal_used, 't')

        self.straw_supply = supply_chain.fit(self.biomass_used[1])

        self.stack = Emitter({self.coal.name: self.coal_used,
                              self.biomass.name: self.biomass_used},
                             self.emission_factor,
                             self.emission_controls)

    def fuel_cost(self):
        cost = self.coal_cost() + self.straw_supply.cost(self.biomass.price)
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        cost = self.coal_om_cost() + self.biomass_om_cost()
        return display_as(cost, 'kUSD')

    def coal_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_coal = (v_after_invest
                         * self.fix_om_coal
                         * self.capacity
                         * (1 - self.biomass_ratio))
        fixed_om_coal[0] = self.fix_om_coal * self.capacity
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = self.power_generation * self.variable_om_coal * (1 - self.biomass_ratio)
        variable_om_coal[0] = self.power_generation[0] * self.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, 'kUSD')

        # Approximation "Small biomass ratio"
        # We don't count the lower O&M work for the coal firing parts of the plant.
    def biomass_om_work(self, OM_hour_MWh):
        time = self.power_generation * self.biomass_ratio * OM_hour_MWh
        return display_as(time, 'hr')

    def biomass_om_wages(self, OM_hour_MWh, wage_operation_maintenance):
        amount = self.biomass_om_work(OM_hour_MWh) * wage_operation_maintenance
        return display_as(amount, 'kUSD')

    def biomass_om_cost(self):
        fixed_om_bm = (v_after_invest
                       * self.fix_om_cost
                       * self.capacity * self.biomass_ratio)
        var_om_bm = (v_after_invest
                     * self.power_generation
                     * self.variable_om_cost
                     * self.biomass_ratio)
        cost = fixed_om_bm + var_om_bm
        return display_as(cost, 'kUSD')

    def cofiring_work(self, OM_hour_MWh, work_hour_day, winder_haul,
                      truck_load, truck_velocity, truck_loading_time):
        """Total work time created from co-firing"""
        time = (self.straw_supply.farm_work(work_hour_day, winder_haul)
                + self.straw_supply.loading_work(truck_loading_time)
                + self.straw_supply.transport_work(truck_load, truck_velocity)
                + self.biomass_om_work(OM_hour_MWh))
        return display_as(time, 'hr')

    def cofiring_wages(self,
                       work_hour_day,
                       winder_haul,
                       wage_bm_collect,
                       truck_load,
                       truck_velocity,
                       wage_bm_transport,
                       truck_loading_time,
                       wage_bm_loading,
                       OM_hour_MWh,
                       wage_operation_maintenance):
        """Total benefit from job creation from biomass co-firing"""
        amount = (self.straw_supply.farm_wages(work_hour_day, winder_haul, wage_bm_collect)
                  + self.straw_supply.transport_wages(truck_load,
                                                      truck_velocity,
                                                      wage_bm_transport)
                  + self.straw_supply.loading_wages(truck_loading_time, wage_bm_loading)
                  + self.biomass_om_wages(OM_hour_MWh, wage_operation_maintenance))
        return display_as(amount, 'kUSD')

    def wages_npv(self,
                  discount_rate,
                  work_hour_day,
                  winder_haul,
                  wage_bm_collect,
                  truck_load,
                  truck_velocity,
                  wage_bm_transport,
                  truck_loading_time,
                  wage_bm_loading,
                  OM_hour_MWh,
                  wage_operation_maintenance):
        v = self.cofiring_wages(work_hour_day,
                                winder_haul,
                                wage_bm_collect,
                                truck_load,
                                truck_velocity,
                                wage_bm_transport,
                                truck_loading_time,
                                wage_bm_loading,
                                OM_hour_MWh,
                                wage_operation_maintenance)
        amount = npv(discount_rate, v)
        return display_as(amount, 'kUSD')

    def coal_saved_cost(self):
        cost = self.coal_saved * self.coal.price
        return display_as(cost, 'kUSD')

    def coal_work_lost(self, mining_productivity):
        time = self.coal_saved / mining_productivity
        return time

    def emission_reduction(self, specific_cost):
        plant_ER = (self.plant.stack.emissions()['Total']
                    - self.stack.emissions()['Total'])
        transport_ER = (self.plant.coal_transporter().emissions()['Total']
                        - self.coal_transporter().emissions()['Total']
                        - self.straw_supply.transport_emissions()['Total'])
        field_ER = (self.straw_supply.field_emission(self.biomass_used[0])['Total']
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
        v = df['CO2']['Benefit']
        value = npv(discount_rate, v)
        return display_as(value, 'kUSD')

    def health_npv(self, discount_rate, specific_cost):
        df = self.emission_reduction(specific_cost)
        v = df.ix['Benefit'].drop('CO2').sum()
        value = npv(discount_rate, v)
        return display_as(value, 'kUSD')

    def tableC(self, feedin_tariff, discount_rate, tax_rate, depreciation_period):
        def printRowInt(label, quantity):
            print('{:30}{:8.0f}'.format(label, quantity))

        def printRowFloat(label, value):
            print('{:30}{:8.4f}'.format(label, value))

        def printRowNPV(label, vector):
            printRowInt(label, npv(discount_rate, vector))

        print("Levelized cost of electricity - ", self.name, "\n")
        printRowInt("Investment", self.capital)
        printRowNPV("Fuel cost", self.fuel_cost())
        printRowNPV("  Coal", self.coal_cost())
        printRowNPV("  Biomass", self.straw_supply.cost(self.biomass.price))
        printRowNPV("    transportation", self.straw_supply.transport_cost())
        printRowNPV("    straw at field", self.straw_supply.field_cost(self.biomass.price))
        printRowNPV("O&M cost", self.operation_maintenance_cost())
        printRowNPV("  coal", self.coal_om_cost())
        printRowNPV("  biomass", self.biomass_om_cost())
        printRowNPV("Tax", self.income_tax(feedin_tariff,
                                           tax_rate,
                                           depreciation_period))
        printRowNPV("Sum of costs", self.cash_out(feedin_tariff,
                                                  tax_rate,
                                                  depreciation_period))
        printRowNPV("Electricity produced", self.power_generation)
        printRowFloat("LCOE", self.lcoe(feedin_tariff,
                                        discount_rate,
                                        tax_rate,
                                        depreciation_period))
