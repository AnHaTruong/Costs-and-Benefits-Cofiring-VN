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
from natu.units import t, y

from init import time_horizon, time_step, v_ones, v_after_invest, display_as, USD
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
                 electricity_tariff,
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
        self.electricity_tariff = electricity_tariff
        self.electricity_tariff.display_unit = 'USD/kWh'
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
        self.esp_efficiency = emission_controls["PM10"]       # To fix in Table 12 and ...
        self.desulfur_efficiency = emission_controls["SO2"]   # To fix in Table 12 and ...
        self.emission_controls = emission_controls
        self.emission_factor = emission_factor

        self.power_generation = full(time_horizon + 1, capacity * capacity_factor, dtype=object)
        self.elec_sale = self.power_generation * time_step
        display_as(self.elec_sale, 'GWh')

        self.boiler_efficiency = full(time_horizon + 1, boiler_efficiency)
        self.plant_efficiency = full(time_horizon + 1, plant_efficiency)

        self.coal_used = self.power_generation / plant_efficiency / coal.heat_value
        display_as(self.coal_used, 't/y')

        self.coal = coal
        self.plant_stack = Emitter({self.coal.name: self.coal_used},
                                   self.emission_factor,
                                   self.emission_controls)
        super().__init__(capital)

    def income(self):
        revenue = self.elec_sale * self.electricity_tariff
        return display_as(revenue, 'kUSD')

    def operating_expenses(self):
        cost = self.fuel_cost() + self.operation_maintenance_cost()
        return display_as(cost, 'kUSD')

    def coal_cost(self):
        # Beware of the non commutative * operator that follows.
        #  leave the scalar quantities rightside and the array leftside
        #  so that natu.py will threads in units inside the array
        cost = self.coal_used * self.coal.price * time_step
        return display_as(cost, 'kUSD')

    def fuel_cost(self):
        return self.coal_cost()

    def coal_om_cost(self):
        fixed_om_coal = full(time_horizon + 1, self.fix_om_coal * self.capacity, dtype=object)
        # Again, the order of the array * scalar operation matters to natu.py
        variable_om_coal = self.power_generation * self.variable_om_coal
        return (fixed_om_coal + variable_om_coal) * time_step

    def operation_maintenance_cost(self):
        return display_as(self.coal_om_cost(), 'kUSD')

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        total_lifetime_power_production = npv(discount_rate, self.elec_sale)
        total_life_cycle_cost = npv(discount_rate, self.cash_out(tax_rate, depreciation_period))
        result = total_life_cycle_cost / total_lifetime_power_production  # * time_step
        result.display_unit = 'USD/kWh'  # Fixme: once TableC is no regression, use /MWh for integer
        return result

    def table_LCOE(self, discount_rate, tax_rate, depreciation_period):
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
        printRowNPV("Tax", self.income_tax(tax_rate, depreciation_period))
        printRowNPV("Sum of costs", self.cash_out(tax_rate, depreciation_period))
        printRowNPV("Electricity produced", self.elec_sale)
        printRowFloat("LCOE", self.lcoe(discount_rate, tax_rate, depreciation_period))
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
            electricity_tariff=plant.electricity_tariff,
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
        self.biomass_heat = v_after_invest * self.gross_heat_input * biomass_ratio
        self.biomass_used = self.biomass_heat / biomass.heat_value
        display_as(self.biomass_used, 't/y')

        self.biomass_used_nan = self.biomass_used.copy()
        for i in range(time_horizon + 1):
            if self.biomass_used[i] == 0 * t / y:
                self.biomass_used_nan[i] = float('nan') * t / y

        self.coal_saved = self.biomass_heat / plant.coal.heat_value
        display_as(self.coal_saved, 't/y')

        self.coal_used = (self.gross_heat_input - self.biomass_heat) / self.coal.heat_value
        display_as(self.coal_used, 't/y')

        self.active_chain = supply_chain.fit(self.biomass_used[1] * time_step)

        self.plant_stack = Emitter({self.coal.name: self.coal_used,
                                    self.biomass.name: self.biomass_used},
                                   self.emission_factor,
                                   self.emission_controls)

    def fuel_cost(self):
        cost = self.coal_cost() + self.biomass_cost()
        return display_as(cost, 'kUSD')

    def biomass_field_cost(self):
        cost = self.biomass_used * self.biomass.price * time_step
        return display_as(cost, 'kUSD')

    def biomass_cost(self):
        cost = self.biomass_field_cost() + self.active_chain.transport_cost()
        return display_as(cost, 'kUSD')

    def biomass_cost_per_t(self):
        """Including transport cost"""
        cost_per_t = self.biomass_cost() / self.biomass_used_nan
        return display_as(cost_per_t, 'USD*y/t')

    def biomass_cost_per_GJ(self):
        cost = self.biomass_cost_per_t() / self.biomass.heat_value / time_step
        return display_as(cost, 'USD / GJ')

    def biomass_transport_cost_per_t(self):
        cost_per_t = self.active_chain.transport_cost() / self.biomass_used_nan
        return display_as(cost_per_t, 'USD*y/t')

    def operation_maintenance_cost(self):
        cost = self.coal_om_cost() + self.biomass_om_cost()
        return display_as(cost, 'kUSD')

    def coal_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_coal = v_after_invest * self.fix_om_coal * self.capacity * (1 - self.biomass_ratio)
        fixed_om_coal[0] = self.fix_om_coal * self.capacity
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = self.power_generation * self.variable_om_coal * (1 - self.biomass_ratio)
        variable_om_coal[0] = self.power_generation[0] * self.variable_om_coal
        cost = (fixed_om_coal + variable_om_coal) * time_step
        return display_as(cost, 'kUSD')

    def biomass_om_cost(self):
        fixed_om_bm = v_ones * self.fix_om_cost * self.capacity * self.biomass_ratio * time_step
        var_om_bm = v_after_invest * self.elec_sale * self.variable_om_cost * self.biomass_ratio
        cost = v_after_invest * (fixed_om_bm + var_om_bm)
        return display_as(cost, 'kUSD')

    def coal_saved_cost(self):
        cost = self.coal_saved * self.coal.price * time_step
        return display_as(cost, 'kUSD')

    def tableC(self, discount_rate, tax_rate, depreciation_period):
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
        printRowNPV("  Biomass", self.biomass_cost())
        printRowNPV("    transportation", self.active_chain.transport_cost())
        printRowNPV("    straw at field", self.biomass_field_cost())
        printRowNPV("O&M cost", self.operation_maintenance_cost())
        printRowNPV("  coal", self.coal_om_cost())
        printRowNPV("  biomass", self.biomass_om_cost())
        printRowNPV("Tax", self.income_tax(tax_rate, depreciation_period))
        printRowNPV("Sum of costs", self.cash_out(tax_rate, depreciation_period))
        printRowNPV("Electricity produced", self.elec_sale)
        printRowFloat("LCOE", self.lcoe(discount_rate, tax_rate, depreciation_period))
