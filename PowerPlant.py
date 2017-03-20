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

from natu.numpy import full, npv

from init import time_horizon, time_step, v_after_invest, display_as, USD
from Investment import Investment
from Emitter import Emitter


class PowerPlant(Investment):
    """ A coal power plant, without co-firing
    """
    def __init__(self,
                 name,
                 capacity,
                 capacity_factor,    # Must be net of self consumption
                 commissioning,
                 boiler_technology,
                 plant_efficiency,
                 boiler_efficiency,
                 fix_om_coal,
                 variable_om_coal,
                 emission_controls,
                 emission_factor,
                 coal,                # type:  Fuel
                 capital=0 * USD
                 ):
        self.name = name
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
        self.emission_controls = emission_controls
        self.emission_factor = emission_factor

        self.power_generation = full(time_horizon + 1,
                                     capacity * capacity_factor * time_step,
                                     dtype=object)
        display_as(self.power_generation, 'GWh')

        self.boiler_efficiency = full(time_horizon + 1, boiler_efficiency)
        self.plant_efficiency = full(time_horizon + 1, plant_efficiency)

        self.coal_used = self.power_generation / plant_efficiency / coal.heat_value
        display_as(self.coal_used, 't')

        self.coal = coal
        self.stack = Emitter({self.coal.name: self.coal_used},
                             self.emission_factor,
                             self.emission_controls)

        self.coal_transport_activity = self.coal_used * 2 * self.coal.transport_distance
        self.coal_transporter = Emitter({self.coal.transport_mean: self.coal_transport_activity},
                                        self.emission_factor
                                        )
        super().__init__(capital)

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

    def coal_transport_emission(self):
        return (self.coal_used[1]
                * self.coal.ef_transport
                * 2 * self.coal.transport_distance   # Trucks do round trip
                )

    def fuel_cost(self):
        return self.coal_cost()

    def coal_om_cost(self):
        fixed_om_coal = full(time_horizon + 1,
                             self.fix_om_coal * self.capacity * time_step,
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
                 plant,             # type: PowerPlant
                 biomass_ratio,
                 capital_cost,
                 fix_om_cost,
                 variable_om_cost,
                 biomass,          # type: Fuel
                 boiler_efficiency_loss,
                 supply_chain
                 ):

        super().__init__(
            name=plant.name + " Cofire",
            capacity=plant.capacity,
            capacity_factor=plant.capacity_factor,
            commissioning=plant.commissioning,
            boiler_technology=plant.boiler_technology,
            plant_efficiency=plant.plant_efficiency[0],
            boiler_efficiency=plant.boiler_efficiency[0],
            fix_om_coal=plant.fix_om_coal,
            variable_om_coal=plant.variable_om_coal,
            coal=plant.coal,
            emission_controls=plant.emission_controls,
            emission_factor=plant.emission_factor,
            capital=capital_cost * plant.capacity * biomass_ratio)

        self.biomass_ratio = biomass_ratio
        self.fix_om_cost = fix_om_cost
        self.variable_om_cost = variable_om_cost
        self.biomass = biomass

        biomass_ratio_mass = biomass_ratio * (plant.coal.heat_value / biomass.heat_value)
        self.boiler_efficiency_loss = boiler_efficiency_loss(biomass_ratio_mass)
        cofiring_boiler_efficiency = (plant.boiler_efficiency - self.boiler_efficiency_loss)

        self.boiler_efficiency = cofiring_boiler_efficiency
        self.boiler_efficiency[0] = plant.boiler_efficiency[0]

        derating = cofiring_boiler_efficiency / plant.boiler_efficiency
        cofiring_plant_efficiency = plant.plant_efficiency * derating

        self.plant_efficiency = cofiring_plant_efficiency
        self.plant_efficiency[0] = plant.plant_efficiency[0]

        self.gross_heat_input = self.power_generation / self.plant_efficiency
        display_as(self.gross_heat_input, 'TJ')

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

        self.coal_transport_activity = self.coal_used * 2 * self.coal.transport_distance
        self.coal_transporter = Emitter({self.coal.transport_mean: self.coal_transport_activity},
                                        self.emission_factor
                                        )

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
                         * self.capacity * time_step
                         * (1 - self.biomass_ratio))
        fixed_om_coal[0] = self.fix_om_coal * self.capacity * time_step
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = self.power_generation * self.variable_om_coal * (1 - self.biomass_ratio)
        variable_om_coal[0] = self.power_generation[0] * self.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, 'kUSD')

    def biomass_om_cost(self):
        # FIXME: the biomass ratio is in HEAT
        fixed_om_bm = (v_after_invest
                       * self.fix_om_cost
                       * self.capacity * time_step * self.biomass_ratio)
        var_om_bm = (v_after_invest
                     * self.power_generation
                     * self.variable_om_cost
                     * self.biomass_ratio)
        cost = fixed_om_bm + var_om_bm
        return display_as(cost, 'kUSD')

    def coal_saved_cost(self):
        cost = self.coal_saved * self.coal.price
        return display_as(cost, 'kUSD')

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
