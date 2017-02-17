# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_horizon, time_step, v_ones, v_after_invest, as_kUSD, USD
from natu.math import sqrt, pi
import natu.numpy as np
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
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.plant_efficiency = plant_efficiency
        self.boiler_efficiency = boiler_efficiency
        self.electricity_tariff = electricity_tariff
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
        self.esp_efficiency = esp_efficiency
        self.desulfur_efficiency = desulfur_efficiency


#        self.power_generation = v_ones.copy() * capacity * capacity_factor
        self.power_generation = np.full(time_horizon+1, capacity * capacity_factor, dtype=object)

        self.coal_used = self.power_generation / plant_efficiency / coal.heat_value
        self.coal_consumption = self.coal_used[0]  # Backward compatibility
        self.elec_sale = self.power_generation * time_step
#        self.elec_sale.display_unit = 'GWh'   # Now vectorized, need to fix Table1 too

        self.coal = coal
        super().__init__(capital)

    def income(self):
        return as_kUSD(self.elec_sale * self.electricity_tariff)

    def operating_expenses(self):
        return as_kUSD(self.fuel_cost() + self.operation_maintenance_cost())

    def fuel_cost(self):
        # natu bugs if in the multiplication,
        # the coal price (scalar) comes before the power generation (vector) ??
        return self.coal_used * self.coal.price * time_step

    def operation_maintenance_cost(self):
#        fixed_om_coal = v_ones.copy() * self.fix_om_coal * self.capacity
        fixed_om_coal = np.full(time_horizon+1, self.fix_om_coal * self.capacity, dtype=object)
        # Same comment:  vector * scalar => okay, scalar * vector => natu.core complains
        variable_om_coal = self.power_generation * self.variable_om_coal
        return (fixed_om_coal + variable_om_coal) * time_step

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        total_lifetime_power_production = np.npv(discount_rate, self.elec_sale)
        total_life_cycle_cost = np.npv(discount_rate, self.cash_out(tax_rate, depreciation_period))
        return total_life_cycle_cost / total_lifetime_power_production * time_step


class CofiringPlant(PowerPlant):
    def __init__(self,
                 plant,             # type: PowerPlant
                 biomass_ratio,
                 capital_cost,
                 fix_om_cost,
                 variable_om_cost,
                 biomass             # type: Fuel
                 ):
        self.biomass_ratio = biomass_ratio

        """Accounting for the efficiency loss due to cofiring, according to Tillman 2000"""
        boiler_efficiency_loss = 0.0044 * biomass_ratio**2 + 0.0055 * biomass_ratio
        cofiring_boiler_efficiency = plant.boiler_efficiency - boiler_efficiency_loss
        cofiring_plant_efficency = (plant.plant_efficiency *
                                    plant.boiler_efficiency / cofiring_boiler_efficiency
                                    )
        super().__init__(
                 capacity=plant.capacity,
                 capacity_factor=plant.capacity_factor,
                 commissioning=plant.commissioning,
                 electricity_tariff=plant.electricity_tariff,
                 fix_om_coal=plant.fix_om_coal,
                 variable_om_coal=plant.variable_om_coal,
                 esp_efficiency=plant.esp_efficiency,
                 desulfur_efficiency=plant.desulfur_efficiency,
                 coal=plant.coal,
                 boiler_technology=plant.boiler_technology,
                 boiler_efficiency=cofiring_boiler_efficiency,
                 plant_efficency=cofiring_plant_efficency,
                 capital=capital_cost * plant.capacity * biomass_ratio
                 )

        self.fix_om_cost = fix_om_cost
        self.variable_om_cost = variable_om_cost
        self.ef_biomass_combust = biomass.ef_combust      # REPLACE AWAY
        self.ef_biomass_transport = biomass.ef_transport  # REPLACE AWAY
        self.biomass_heat_value = biomass.heat_value      # REPLACE AWAY
        self.biomass = biomass

        self.gross_heat_input = self.power_generation / self.plant_efficency
        self.biomass_heat = v_after_invest * self.gross_heat_input * biomass_ratio
        self.biomass_used = self.biomass_heat / biomass.heat_value

        self.coal_saved = self.biomass_heat / plant.coal.heat_value
        self.coal_used -= self.coal_saved

    def fuel_cost(self):
        return self.coal_cost() + self.biomass_cost() + self.biomass_transport_cost()

    def coal_cost(self):
        return self.coal.price * self.coal_used * time_step

    def coal_saved_cost(self):
        return self.coal_price * self.coal_saved * time_step

    def biomass_cost(self):
        return self.biomass.price * self.biomass_used * time_step

# RESUME WORK HERE

    def biomass_transport_cost(self,
                               biomass_quantity,
                               transport_tariff,
                               biomass_density,
                               tortuosity_factor
                               ):
        return (v_after_invest * transport_tariff *
                self.biomass_transport(biomass_quantity, biomass_density, tortuosity_factor)
                )

    # For now, the disc case (Ninh Binh)
    def biomass_transport(self, quantity, density, tortuosity_factor):
        area = quantity / density
        radius = sqrt(area / pi)
        return tortuosity_factor * density * pi * radius**3 / 3

    def operation_maintenance_cost(self,
                                   biomass_fix_cost,
                                   transport_tariff,
                                   biomass_density,
                                   tortuosity_factor
                                   ):
        return (self.plant.operating_expenses() -
                self.coal_saved_cost() +
                self.biomass_fuel_cost(biomass_fix_cost) +
                self.biomass_om_costs() +
                self.biomass_transport_cost(self.biomass_used(),
                                            transport_tariff,
                                            biomass_density,
                                            tortuosity_factor
                                            )
                )

    def biomass_om_costs(self):
        fixed_om_bm = self.fix_om_cost * self.plant.capacity * self.biomass_ratio * time_step
        variable_om_bm = self.variable_om_cost * self.plant.elec_sale * self.biomass_ratio
        return v_after_invest * (fixed_om_bm + variable_om_bm)

