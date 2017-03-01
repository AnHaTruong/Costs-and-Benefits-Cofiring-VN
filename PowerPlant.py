# Economic of co-firing in two power plants in Vietnam
#
# A Power plant
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_horizon, time_step, v_ones, v_after_invest, display_as, USD
import natu.numpy as np
from natu.units import t, y
from Investment import Investment


class Fuel:
    def __init__(self,
                 heat_value,
                 price,
                 transport_distance,
                 ef_combust,
                 ef_transport,
                 ef_so2,
                 ef_pm10,
                 ef_nox
                 ):
        self.heat_value = heat_value
        self.price = price
        self.price.display_unit = 'USD/t'
        self.transport_distance = transport_distance
        self.ef_combust = ef_combust
        self.ef_transport = ef_transport
        self.ef_so2 = ef_so2
        self.ef_pm10 = ef_pm10
        self.ef_nox = ef_nox


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
                 esp_efficiency,
                 desulfur_efficiency,
                 coal,                # type:  Fuel
                 capital=0*USD
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
        self.esp_efficiency = esp_efficiency
        self.desulfur_efficiency = desulfur_efficiency

        # Backward compatibility
        self.coal_consumption = capacity * capacity_factor / plant_efficiency / coal.heat_value

        self.power_generation = np.full(time_horizon+1, capacity * capacity_factor, dtype=object)
        self.elec_sale = self.power_generation * time_step
        display_as(self.elec_sale, 'GWh')

        self.plant_efficiency = np.full(time_horizon+1, plant_efficiency)
        self.boiler_efficiency = np.full(time_horizon+1, boiler_efficiency)

        self.coal = coal
        super().__init__(capital)

    def coal_used(self):
        mass = self.power_generation / self.plant_efficiency / self.coal.heat_value
        return display_as(mass, 't/y')

    def income(self):
        return display_as(self.elec_sale * self.electricity_tariff, 'kUSD')

    def operating_expenses(self):
        return display_as(self.fuel_cost() + self.operation_maintenance_cost(), 'kUSD')

    def coal_cost(self):
        # natu bugs if in the multiplication,
        # the coal price (scalar) comes before the power generation (vector) ??
        return self.coal_used() * self.coal.price * time_step

    def fuel_cost(self):
        return self.coal_cost()

    def operation_maintenance_cost(self):
        # fixed_om_coal = v_ones.copy() * self.fix_om_coal * self.capacity
        fixed_om_coal = np.full(time_horizon+1, self.fix_om_coal * self.capacity, dtype=object)
        # Same comment:  vector * scalar => okay, scalar * vector => natu.core complains
        variable_om_coal = self.power_generation * self.variable_om_coal
        return (fixed_om_coal + variable_om_coal) * time_step

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        total_lifetime_power_production = np.npv(discount_rate, self.elec_sale)
        total_life_cycle_cost = np.npv(discount_rate, self.cash_out(tax_rate, depreciation_period))
        result = total_life_cycle_cost / total_lifetime_power_production  # * time_step
        result.display_unit = 'USD/kWh'  # Fixme: once TableC is no regression, use /MWh for integer
        return result


def boiler_efficiency_loss(biomass_ratio_mass):
    """Boiler efficiency loss due to cofiring, according to Tillman 2000"""
    return 0.0044 * biomass_ratio_mass**2 + 0.0055 * biomass_ratio_mass


class CofiringPlant(PowerPlant):

    def __init__(self,
                 plant,             # type: PowerPlant
                 biomass_ratio,
                 capital_cost,
                 fix_om_cost,
                 variable_om_cost,
                 biomass,             # type: Fuel
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
                 esp_efficiency=plant.esp_efficiency,
                 desulfur_efficiency=plant.desulfur_efficiency,
                 coal=plant.coal,
                 capital=capital_cost * plant.capacity * biomass_ratio
                 )

        self.biomass_ratio = biomass_ratio
        self.fix_om_cost = fix_om_cost
        self.variable_om_cost = variable_om_cost
        self.ef_biomass_combust = biomass.ef_combust      # REPLACE AWAY
        self.ef_biomass_transport = biomass.ef_transport  # REPLACE AWAY
        self.biomass_heat_value = biomass.heat_value      # REPLACE AWAY
        self.biomass = biomass
        self.supply_chain = supply_chain

        biomass_ratio_mass = biomass_ratio * (plant.coal.heat_value/biomass.heat_value)
        cofiring_boiler_efficiency = (plant.boiler_efficiency -
                                      boiler_efficiency_loss(biomass_ratio_mass)
                                      )
        # TODO: use vector algebra in case investment takes more than 1 period
        self.boiler_efficiency = cofiring_boiler_efficiency
        self.boiler_efficiency[0] = plant.boiler_efficiency[0]

        derating = cofiring_boiler_efficiency / plant.boiler_efficiency
        cofiring_plant_efficiency = plant.plant_efficiency * derating
        # TODO: use vector algebra in case investment takes more than 1 period
        self.plant_efficiency = cofiring_plant_efficiency
        self.plant_efficiency[0] = plant.plant_efficiency[0]

        self.gross_heat_input = self.power_generation / self.plant_efficiency
        self.biomass_heat = v_after_invest * self.gross_heat_input * biomass_ratio
        self.biomass_used = self.biomass_heat / biomass.heat_value
        display_as(self.biomass_used, 't/y')

        self.biomass_used_nan = self.biomass_used.copy()
        for i in range(time_horizon + 1):
            if self.biomass_used[i] == 0 * t/y:
                self.biomass_used_nan[i] = float('nan') * t/y

        self.coal_saved = self.biomass_heat / plant.coal.heat_value
        display_as(self.coal_saved, 't/y')

    def coal_used(self):
        mass = self.power_generation / self.plant_efficiency / self.coal.heat_value
        mass = mass - self.coal_saved
        return display_as(mass, 't/y')

    def fuel_cost(self):
        cost = self.coal_cost() + self.biomass_cost()
        return display_as(cost, 'kUSD')

    def biomass_cost(self):
        cost = (self.biomass_used * self.biomass.price * time_step +
                self.supply_chain.v_transport_cost(self.biomass_used)
                )
        return display_as(cost, 'kUSD')

    def biomass_cost_per_t(self):
        cost_per_t = self.biomass_cost() / self.biomass_used_nan
        return display_as(cost_per_t, 'USD*y/t')

    def biomass_transport_cost_per_t(self):
        cost_per_t = (self.supply_chain.v_transport_cost(self.biomass_used) /
                      self.biomass_used_nan
                      )
        return display_as(cost_per_t, 'USD*y/t')

    def operation_maintenance_cost(self):
        cost = super().operation_maintenance_cost() + self.biomass_om_cost()
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
        def printRowInt(label, quantity, unit='kUSD'):
            quantity.display_unit = unit
            print('{:30}{:8.0f}'.format(label, quantity))
            return None

        def printRowFloat(label, value):
            print('{:30}{:8.4f}'.format(label, value))
            return None

        def printRowNPV(label, vector, unit='kUSD'):
            printRowInt(label, np.npv(discount_rate, vector), unit)

        print("Levelized cost of electricity - ", self.name, "\n")
        printRowInt("Investment", self.capital)
        printRowNPV("Fuel cost: Coal", super().fuel_cost())
        printRowNPV("Fuel cost: Biomass", self.biomass_cost())
        printRowNPV("O&M cost", self.operation_maintenance_cost())
        printRowNPV("Tax", self.income_tax(tax_rate, depreciation_period))
        printRowNPV("Sum of costs", self.cash_out(tax_rate, depreciation_period))
        printRowNPV("Electricity produced", self.elec_sale, 'GWh')
        printRowFloat("LCOE", self.lcoe(discount_rate, tax_rate, depreciation_period))
