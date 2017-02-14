# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_step, time_horizon
import natu.numpy as np
from natu.math import sqrt, pi


v_zeros = np.zeros(time_horizon + 1, dtype=np.float64)
v_ones = np.ones(time_horizon + 1, dtype=np.float64)
v_after_invest = np.ones(time_horizon + 1, dtype=np.float64)
v_after_invest[0] = 0


class Investment:
    """An investment of capital paid in period 0,
        There are income, operating expenses and taxes in subsequent periods
        Taxes account for linear amortization of the capital starting period 1
        No salvage value
       Virtual class,
        descendent class should redefine  income()  and  operating_expense()
        These functions should return a vector of numbers like v_zeros
    """
    def __init__(self, capital=0):
        self.capital = capital
        self.investment = v_zeros.copy()
        self.investment[0] = capital

    def income(self):
        return v_zeros

    def operating_expenses(self):
        return v_zeros

    def amortization(self, depreciation_period):
        assert type(depreciation_period) is int, "Depreciation period not an integer"
        assert 0 < depreciation_period < time_horizon - 1, "Depreciation not in {1..timehorizon-1}"
        v_cost = v_zeros.copy()
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.capital / float(depreciation_period)
        return v_cost

    def earning_before_tax(self, depreciation_period):
        return (self.income() -
                self.operating_expenses() -
                self.amortization(depreciation_period)
                )

    def income_tax(self, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        return tax_rate * self.earning_before_tax(depreciation_period)

    def net_cash_flow(self, tax_rate, depreciation_period):
        return (self.income() -
                self.investment -
                self.operating_expenses() -
                self.income_tax(tax_rate, depreciation_period)
                )

    def net_present_value(self, discount_rate, tax_rate, depreciation_period):
        assert 0 <= discount_rate < 1, "Discount rate not in [0, 1["
        return np.npv(discount_rate, self.net_cash_flow(tax_rate, depreciation_period))


class PowerPlant(Investment):
    """ A coal power plant, without co-firing
    """
    def __init__(self,
                 capacity,
                 capacity_factor,
                 commissioning,
                 boiler_technology,
                 coal_heat_value,
                 plant_efficiency,
                 boiler_efficiency,
                 electricity_tariff,
                 coal_price,
                 fix_om_coal,
                 variable_om_coal,
                 ef_coal_combust,
                 ef_coal_transport,
                 coal_transport_distance,
                 esp_efficiency,
                 desulfur_efficiency,
                 ef_so2_coal,
                 ef_pm10_coal,
                 ef_nox_coal
                 ):
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.power_generation = capacity * capacity_factor * time_step
        self.coal_heat_value = coal_heat_value
        self.plant_efficiency = plant_efficiency
        self.boiler_efficiency = boiler_efficiency
        self.base_coal_consumption = capacity * capacity_factor / plant_efficiency / coal_heat_value
        self.electricity_tariff = electricity_tariff
        self.coal_price = coal_price
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
        self.elec_sale = self.power_generation  # Capacity factor was net of self consumption
        self.ef_coal_combust = ef_coal_combust
        self.ef_coal_transport = ef_coal_transport
        self.coal_transport_distance = coal_transport_distance
        self.esp_efficiency = esp_efficiency  # FIXME: keep depollution related code separate
        self.desulfur_efficiency = desulfur_efficiency
        self.ef_so2_coal = ef_so2_coal
        self.ef_pm10_coal = ef_pm10_coal
        self.ef_nox_coal = ef_nox_coal

    def income(self):
        return v_ones * self.elec_sale * self.electricity_tariff

    def operating_expenses(self):
        return self.v_fuel_cost() + self.v_operation_maintenance_cost()

    def v_fuel_cost(self):
        return v_ones * self.coal_price * self.base_coal_consumption * time_step

    def v_operation_maintenance_cost(self):
        v_fixed_om_coal = v_ones * self.fix_om_coal * self.capacity * time_step
        v_variable_om_coal = v_ones * self.variable_om_coal * self.power_generation
        return v_fixed_om_coal + v_variable_om_coal

    def v_discounted_total_power_gen(self, discount_rate):
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

    def v_operation_maintenance_cost(self,
                                     biomass_fix_cost,
                                     transport_tariff,
                                     biomass_density,
                                     tortuosity_factor):
        return (self.plant.operating_expenses() -
                self.coal_saved_cost() +
                self.biomass_fuel_cost(biomass_fix_cost) +
                self.biomass_om_costs() +
                self.biomass_transport_cost(self.biomass_used(),
                                            transport_tariff,
                                            biomass_density,
                                            tortuosity_factor)
                )

    def biomass_heat(self):
        """Accounting for the efficiency loss due to cofiring, according to Tillman 2000"""
        boiler_efficiency_loss = 0.0044 * self.biomass_ratio**2 + 0.0055 * self.biomass_ratio #FIXME: update from Ha's repo
        new_boiler_efficiency = self.plant.boiler_efficiency - boiler_efficiency_loss
        new_plant_efficency = (self.plant.plant_efficiency *
                               self.plant.boiler_efficiency / new_boiler_efficiency
                               )
        gross_heat_input = self.plant.power_generation / new_plant_efficency / time_step
        return v_after_invest * gross_heat_input * self.biomass_ratio

    def coal_saved(self):
        return self.biomass_heat() / self.plant.coal_heat_value

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
                               tortuosity_factor):
        return (v_after_invest * transport_tariff *
                self.biomass_transport(biomass_quantity, biomass_density, tortuosity_factor)
                )

    # For now, the disc case (Ninh Binh)
    def biomass_transport(self, quantity, density, tortuosity_factor):
        area = quantity / density
        radius = sqrt(area / pi)
        return tortuosity_factor * density * pi * radius**3 / 3
