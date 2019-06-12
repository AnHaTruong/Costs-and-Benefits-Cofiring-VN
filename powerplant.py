# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A Power plant
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Define PowerPlant, FuelPowerPlant and CofiringPlant."""

import pandas as pd
import numpy as np

from natu.units import y
from natu.numpy import npv

from init import USD, MUSD, display_as, safe_divide
from investment import Investment
from emitter import Emitter, Activity


class PowerPlant(Investment):
    """A power plant, without specific technology."""

    def __init__(self,
                 parameter,
                 capital=0 * USD):
        """Initialize the power plant.

        Technology agnostic.
        """
        Investment.__init__(self, parameter.name, parameter.time_horizon, capital)
        self.parameter = parameter

        self.power_generation = (np.ones(parameter.time_horizon + 1) *
                                 parameter.capacity * parameter.capacity_factor * y)
        display_as(self.power_generation, 'GWh')

    def operating_expenses(self):
        cost = self.operation_maintenance_cost()
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        """Return the vector of operation and maintenance cost."""
        fixed_om = (np.ones(self.parameter.time_horizon + 1) *
                    self.parameter.fixed_om * self.parameter.capacity * y)
        variable_om = self.power_generation * self.parameter.variable_om
        cost = fixed_om + variable_om
        return display_as(cost, 'kUSD')

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        """Return the levelized cost of electricity, taxes included."""
        total_lifetime_power_production = npv(discount_rate, self.power_generation)
        total_life_cycle_cost = npv(discount_rate,
                                    self.cash_out(tax_rate, depreciation_period))
        result = total_life_cycle_cost / total_lifetime_power_production
        return display_as(result, 'USD/MWh')

    def characteristics(self):
        """Describe the technical characteristics of the plant."""
        description = pd.Series(name=self.parameter.name)
        description["Comissioning year"] = self.parameter.commissioning
        description["Installed capacity"] = self.parameter.capacity
        return description

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = pd.Series(name=self.name)
        statement["Investment    (MUSD)"] = self.capital / MUSD
        statement["O&M cost      (MUSD)"] = npv(
            discount_rate, self.operation_maintenance_cost()) / MUSD
        statement["Tax           (MUSD)"] = npv(
            discount_rate, self.income_tax(tax_rate, depreciation_period)) / MUSD
        statement["Cash_out      (MUSD)"] = npv(
            discount_rate,
            self.cash_out(tax_rate, depreciation_period)) / MUSD
        statement["Electricity produced"] = npv(
            discount_rate, self.power_generation)
        statement["LCOE                "] = self.lcoe(
            discount_rate, tax_rate, depreciation_period)
        return statement


#pylint: disable=too-many-instance-attributes
class FuelPowerPlant(PowerPlant, Emitter):
    """A power plant using a single fuel, like coal or gas, without co-firing."""

    def __init__(self,
                 parameter,
                 derating=None,
                 capital=0 * USD):
        """Initialize the power plant, compute the amount of fuel used.

        The financials (revenue and fuel_cost) are not initialized at this time,
        they must be defined later:

        >>> from parameters import plant_parameter_MD1, price_MD1
        >>> plant = FuelPowerPlant(plant_parameter_MD1)
        >>> plant.revenue = plant.power_generation * price_MD1.electricity
        >>> plant.operating_expenses()
        Traceback (most recent call last):
            ...
        AttributeError: Accessing  FuelPowerPlant.fuel_cost  value before it is set

        >>> plant.fuel_cost = plant.fuel_used * price_MD1.coal
        >>> print(plant.net_present_value(discount_rate=0.08))
        1.29299e+06 kUSD

        The capital cost is zero in this case
        """
        PowerPlant.__init__(self, parameter, capital)

        if derating is not None:
            self.derating = derating
        else:
            self.derating = np.ones(parameter.time_horizon + 1)
        self.plant_efficiency = parameter.plant_efficiency * self.derating

        self.gross_heat_input = self.power_generation / self.plant_efficiency
        display_as(self.gross_heat_input, 'TJ')

        self.fuel_used = self.gross_heat_input / parameter.fuel.heat_value
        display_as(self.fuel_used, parameter.fuel.unit)

        Emitter.__init__(self,
                         Activity(name=parameter.fuel.name,
                                  level=self.fuel_used,
                                  emission_factor=parameter.emission_factor[parameter.fuel.name]),
                         emission_control=parameter.emission_control)

        self._fuel_cost = None

    @property
    def fuel_cost(self):
        if self._fuel_cost is None:
            raise AttributeError('Accessing  FuelPowerPlant.fuel_cost  value before it is set')
        return display_as(self._fuel_cost, 'kUSD')

    @fuel_cost.setter
    def fuel_cost(self, value):
        self._fuel_cost = value

    def all_fuel_cost(self):
        return self.fuel_cost

    def operating_expenses(self):
        cost = self.all_fuel_cost() + self.operation_maintenance_cost()
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        return display_as(self.fuel_om_cost(), 'kUSD')

    def fuel_om_cost(self):
        return PowerPlant.operation_maintenance_cost(self)

    def fuel_transport_tkm(self):
        return self.fuel_used * 2 * self.parameter.fuel.transport_distance   # Return trip inputed

    def fuel_transporter(self):
        """Return an Emitter object to access emissions from coal transport."""
        transport_mean = self.parameter.fuel.transport_mean
        activity = Activity(
            name=transport_mean,
            level=self.fuel_transport_tkm(),
            emission_factor=self.parameter.emission_factor[transport_mean])
        return Emitter(activity)

    def characteristics(self):
        """Describe the technical characteristics of the plant."""
        description = PowerPlant.characteristics(self)
        description["Boiler technology"] = self.parameter.boiler_technology
        description["Capacity factor"] = self.parameter.capacity_factor
        description["Fuel consumption"] = self.fuel_used[1]
        description["Heat value of fuel"] = self.parameter.fuel.heat_value
        description["Plant efficiency"] = self.plant_efficiency[1]
        description["Boiler efficiency"] = self.parameter.boiler_efficiency_new
        return description

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
 #       statement = PowerPlant.lcoe_statement(self, discount_rate, tax_rate, depreciation_period)
        statement = pd.Series(name=self.name)
        statement["Investment    (MUSD)"] = self.capital / MUSD
        statement["Fuel cost     (MUSD)"] = npv(discount_rate, self.all_fuel_cost()) / MUSD
        statement["  Coal        (MUSD)"] = npv(discount_rate, self.fuel_cost) / MUSD
        statement["  Biomass     (MUSD)"] = 0
        statement["O&M cost      (MUSD)"] = npv(
            discount_rate, self.operation_maintenance_cost()) / MUSD
        statement["  O&M coal    (MUSD)"] = npv(
            discount_rate, self.fuel_om_cost()) / MUSD
        statement["  O&M biomass (MUSD)"] = 0
        statement["Tax           (MUSD)"] = npv(
            discount_rate, self.income_tax(tax_rate, depreciation_period)) / MUSD
        statement["Cash_out      (MUSD)"] = npv(
            discount_rate,
            self.cash_out(tax_rate, depreciation_period)) / MUSD
        statement["Electricity produced"] = npv(
            discount_rate, self.power_generation)
        statement["LCOE                "] = self.lcoe(
            discount_rate, tax_rate, depreciation_period)
        return statement


class CofiringPlant(FuelPowerPlant):
    """A power plant which co-fires biomass with a main fuel."""

    def __init__(self, plant_parameter, cofire_parameter):
        """Initialize the cofiring plant.

        1/ Instanciate as a FuelPowerPlant with a lower efficiency and higher capital cost
        2/ Compute the biomass used and coal saved
        3/ Overwrite the list of activities from grandparent class Emitter.

        The financials (revenue, fuel_cost, biomass_cost) are not initialized at this time,
        they must be defined later:

        >>> from parameters import plant_parameter_MD1, cofire_MD1, price_MD1
        >>> plant = CofiringPlant(plant_parameter_MD1, cofire_MD1)
        >>> plant.revenue = plant.power_generation * price_MD1.electricity
        >>> plant.fuel_cost = plant.fuel_used * price_MD1.coal # free transport in test
        >>> plant.operating_expenses()
        Traceback (most recent call last):
            ...
        AttributeError: Accessing  CofiringPlant.biomass_cost  value before it is set

        >>> plant.biomass_cost = plant.biomass_used * price_MD1.biomass
        >>> print(plant.net_present_value(discount_rate=0.08))
        1.26988e+06 kUSD

        """
        self.cofire_parameter = cofire_parameter

        biomass_ratio_mass = (cofire_parameter.biomass_ratio_energy
                              * plant_parameter.fuel.heat_value
                              / cofire_parameter.biomass.heat_value)

        boiler_efficiency = (np.ones(plant_parameter.time_horizon + 1) *
                             plant_parameter.boiler_efficiency_new
                             - cofire_parameter.boiler_efficiency_loss(biomass_ratio_mass))
        boiler_efficiency[0] = plant_parameter.boiler_efficiency_new

        FuelPowerPlant.__init__(
            self,
            plant_parameter,
            derating=boiler_efficiency / plant_parameter.boiler_efficiency_new,
            capital=(cofire_parameter.capital_cost
                     * plant_parameter.capacity * y
                     * float(cofire_parameter.biomass_ratio_energy[1])))

        self.name = plant_parameter.name + ' Cofire'

        biomass_heat = self.gross_heat_input * self.cofire_parameter.biomass_ratio_energy

        self.biomass_used = biomass_heat / cofire_parameter.biomass.heat_value
        display_as(self.biomass_used, 't')

        self.fuel_saved = biomass_heat / plant_parameter.fuel.heat_value

        self.fuel_used -= self.fuel_saved

        self.activities = [
            Activity(
                name=plant_parameter.fuel.name,
                level=self.fuel_used,
                emission_factor=plant_parameter.emission_factor[plant_parameter.fuel.name]),
            Activity(
                name='Straw',
                level=self.biomass_used,
                emission_factor=plant_parameter.emission_factor[cofire_parameter.biomass.name])]

        self._biomass_cost = None

    @property
    def biomass_cost(self):
        if self._biomass_cost is None:
            raise AttributeError('Accessing  CofiringPlant.biomass_cost  value before it is set')
        return display_as(self._biomass_cost, 'kUSD')

    @biomass_cost.setter
    def biomass_cost(self, value):
        self._biomass_cost = value

    def biomass_cost_per_t(self):
        return safe_divide(self.biomass_cost, self.biomass_used)

    def biomass_energy_cost(self):
        cost = self.biomass_cost_per_t() / self.cofire_parameter.biomass.heat_value
        return display_as(cost, 'USD / GJ')

    def all_fuel_cost(self):
        cost = self.fuel_cost + self.biomass_cost
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        cost = self.fuel_om_cost() + self.biomass_om_cost()
        return display_as(cost, 'kUSD')

    def fuel_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_fuel = ((1 - self.cofire_parameter.biomass_ratio_energy)
                         * self.parameter.fixed_om
                         * self.parameter.capacity * y)
        # Variable costs proportional to generation after capacity factor
        variable_om_fuel = ((1 - self.cofire_parameter.biomass_ratio_energy)
                            * self.power_generation
                            * self.parameter.variable_om)
        cost = fixed_om_fuel + variable_om_fuel
        return display_as(cost, 'kUSD')

        # Approximation "Small biomass ratio"
        # We don't count the lower O&M work for the coal firing parts of the plant.
    def biomass_om_work(self):
        time = (self.power_generation
                * self.cofire_parameter.biomass_ratio_energy
                * self.cofire_parameter.OM_hour_MWh)
        return display_as(time, 'hr')

    def biomass_om_wages(self):
        amount = self.biomass_om_work() * self.cofire_parameter.wage_operation_maintenance
        return display_as(amount, 'kUSD')

    def biomass_om_cost(self):
        """Return  Operation and Maintenance costs of the biomass cofiring part of the plant."""
        fixed_om_bm = (self.cofire_parameter.biomass_ratio_energy
                       * self.cofire_parameter.fix_om_cost
                       * self.parameter.capacity * y)
        var_om_bm = (self.cofire_parameter.biomass_ratio_energy
                     * self.power_generation
                     * self.cofire_parameter.variable_om_cost)
        cost = fixed_om_bm + var_om_bm
        # error_message = "Biomass O&M variable costs appear lower than biomass OM wages."
        # assert var_om_bm[1] > self.biomass_om_wages()[1], error_message
        return display_as(cost, 'kUSD')

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = FuelPowerPlant.lcoe_statement(self,
                                                  discount_rate, tax_rate, depreciation_period)
        statement["  Biomass     (MUSD)"] = npv(discount_rate, self.biomass_cost) / MUSD
        statement["  O&M biomass (MUSD)"] = npv(discount_rate, self.biomass_om_cost()) / MUSD
        return statement
