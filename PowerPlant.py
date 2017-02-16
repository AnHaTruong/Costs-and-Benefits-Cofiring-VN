# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_step, v_ones, v_after_invest, as_kUSD
from natu.math import sqrt, pi
import natu.numpy as np
from Investment import Investment


class EmissionsControls:
    def __init__(self,
                 esp_efficiency,
                 desulfur_efficiency,
                 ef_coal_combust,
                 ef_coal_transport,
                 ef_so2_coal,
                 ef_pm10_coal,
                 ef_nox_coal
                 ):
        self.ef_coal_combust = ef_coal_combust
        self.ef_coal_transport = ef_coal_transport
        self.esp_efficiency = esp_efficiency
        self.desulfur_efficiency = desulfur_efficiency
        self.ef_so2_coal = ef_so2_coal
        self.ef_pm10_coal = ef_pm10_coal
        self.ef_nox_coal = ef_nox_coal


class CoalSupply:
    def __init__(self,
               heat_value,
               price,
               transport_distance
               ):
        self.heat_value = heat_value
        self.price = price
        self.transport_distance = transport_distance


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
                 coal_supply,
                 emissions_controls
                 ):
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.power_generation = capacity * capacity_factor
        self.plant_efficiency = plant_efficiency
        self.boiler_efficiency = boiler_efficiency
        self.coal_consumption = self.power_generation / plant_efficiency / coal_supply.heat_value
        self.electricity_tariff = electricity_tariff
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
        self.elec_sale = self.power_generation * time_step
        self.elec_sale.display_unit = 'GWh'
        self.coal_supply = coal_supply
        self.emissions_controls = emissions_controls
        super().__init__()

    def income(self):
        return as_kUSD(v_ones * self.elec_sale * self.electricity_tariff)

    def operating_expenses(self):
        return as_kUSD(self.fuel_cost() + self.operation_maintenance_cost())

    def fuel_cost(self):
        return v_ones * self.coal_supply.price * self.coal_consumption * time_step

    def operation_maintenance_cost(self):
        fixed_om_coal = v_ones * self.fix_om_coal * self.capacity * time_step
        variable_om_coal = v_ones * self.variable_om_coal * self.power_generation * time_step
        return fixed_om_coal + variable_om_coal

    def discounted_total_power_gen(self, discount_rate):
        return np.npv(discount_rate, self.v_sales)


class CofiringProject(Investment):
    def __init__(self,
                 plant,
                 biomass_ratio,
                 capital_cost,
                 fix_om_cost,
                 variable_om_cost,
                 ef_biomass_combust,
                 ef_biomass_transport,
                 biomass_heat_value
                 ):
        self.plant = plant
#        self.capital_cost = capital_cost
        self.capital = capital_cost * plant.capacity * biomass_ratio
        super().__init__(self.capital)
        self.fix_om_cost = fix_om_cost
        self.variable_om_cost = variable_om_cost
        self.ef_biomass_combust = ef_biomass_combust
        self.ef_biomass_transport = ef_biomass_transport
        self.biomass_heat_value = biomass_heat_value

    def income(self):
        return self.plant.income()

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

    def biomass_heat(self):
        """Accounting for the efficiency loss due to cofiring, according to Tillman 2000"""
        boiler_efficiency_loss = 0.0044 * self.biomass_ratio**2 + 0.0055 * self.biomass_ratio
        new_boiler_efficiency = self.plant.boiler_efficiency - boiler_efficiency_loss
        new_plant_efficency = (self.plant.plant_efficiency *
                               self.plant.boiler_efficiency / new_boiler_efficiency
                               )
        gross_heat_input = self.plant.power_generation / new_plant_efficency
        return v_after_invest * gross_heat_input * self.biomass_ratio

    def coal_saved(self):
        return self.biomass_heat() / self.plant.coal_supply.heat_value

    def coal_saved_cost(self):
        return self.plant.coal_price * self.coal_saved() * time_step

    def biomass_used(self):
        return self.biomass_heat() / self.biomass_heat_value

    def biomass_fuel_cost(self, biomass_fix_cost):
        return biomass_fix_cost * self.biomass_used() * time_step

    def biomass_om_costs(self):
        fixed_om_bm = self.fix_om_cost * self.plant.capacity * self.biomass_ratio * time_step
        variable_om_bm = self.variable_om_cost * self.plant.elec_sale * self.biomass_ratio
        return v_after_invest * (fixed_om_bm + variable_om_bm)

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
