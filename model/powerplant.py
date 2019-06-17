# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A Power plant
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Define PowerPlant and its child class, CofiringPlant."""

from collections import namedtuple

import pandas as pd
import numpy as np

from natu.units import y
from natu.numpy import npv

from model.utils import USD, MUSD, display_as, safe_divide
from model.investment import Investment
from model.emitter import Emitter, Activity


Fuel = namedtuple('Fuel', 'name, heat_value, transport_distance, transport_mean')

PlantParameter = namedtuple("PlantParameter", ['name',
                                               'capacity',
                                               'capacity_factor',
                                               'commissioning',
                                               'boiler_technology',
                                               'boiler_efficiency_new',
                                               'plant_efficiency',
                                               'fix_om_coal',
                                               'variable_om_coal',
                                               'emission_factor',
                                               'emission_control',
                                               'coal',
                                               'time_horizon'])

CofiringParameter = namedtuple('CofiringParameter', ['biomass_ratio_energy',
                                                     'capital_cost',
                                                     'fix_om_cost',
                                                     'variable_om_cost',
                                                     'biomass',
                                                     'boiler_efficiency_loss',
                                                     'OM_hour_MWh',
                                                     'wage_operation_maintenance'])


#pylint: disable=too-many-instance-attributes
class PowerPlant(Investment, Emitter):
    """A coal power plant, without co-firing."""

    def __init__(self,
                 parameter,
                 derating=None,
                 capital=0 * USD):
        """Initialize the power plant, compute the amount of coal used.

        The financials (revenue and coal_cost) are not initialized at this time,
        they must be defined later:

        >>> from model.utils import VND
        >>> from natu.units import t, km, kg, kWh, kW, MW, MJ
        >>> plant_parameter_MD1 = PlantParameter(name='Mong Duong 1',
        ...                                      capacity=1080 * MW,
        ...                                      capacity_factor=0.60,
        ...                                      commissioning=2015,
        ...                                      boiler_technology='CFB',
        ...                                      boiler_efficiency_new=87.03 / 100,
        ...                                      plant_efficiency=38.84 / 100,
        ...                                      fix_om_coal=29.31 * USD / kW / y,
        ...                                      variable_om_coal=0.0048 * USD / kWh,
        ...                                      emission_factor={'6b_coal': {
        ...                                         'CO2': 0.0966 * kg / MJ * 19.43468 * MJ / kg,
        ...                                         'SO2': 11.5 * kg / t,
        ...                                         'NOx': 18 * kg / t,
        ...                                         'PM10': 43.8 * kg / t}},
        ...                                      emission_control={'CO2': 0.0,
        ...                                                        'SO2': 0.982,
        ...                                                        'NOx': 0.0,
        ...                                                        'PM10': 0.996},
        ...                                      coal=Fuel(name="6b_coal",
        ...                                                heat_value=19.43468 * MJ / kg,
        ...                                                transport_distance=0 * km,
        ...                                                transport_mean='Conveyor belt'),
        ...                                      time_horizon=20)
        >>> plant = PowerPlant(plant_parameter_MD1)
        >>> from model.system import Price
        >>> price_MD1 = Price(biomass=37.26 * USD / t,
        ...                   transport=2000 * VND / t / km,
        ...                   coal=1131400 * VND / t,
        ...                   electricity=1239.17 * VND / kWh)
        >>> plant.revenue = plant.power_generation * price_MD1.electricity
        >>> plant.operating_expenses()
        Traceback (most recent call last):
            ...
        AttributeError: Accessing  PowerPlant.coal_cost  value before it is set
        >>> plant.coal_cost = plant.coal_used * price_MD1.coal
        >>> print(plant.net_present_value(discount_rate=0.08))
        1.29299e+06 kUSD

        The capital cost represents the cost of installing cofiring,
        it is zero in this case.
        """
        Investment.__init__(self, parameter.name, parameter.time_horizon, capital)
        self.parameter = parameter

        self.power_generation = (np.ones(parameter.time_horizon + 1) *
                                 parameter.capacity * parameter.capacity_factor * y)
        display_as(self.power_generation, 'GWh')

        if derating is not None:
            self.derating = derating
        else:
            self.derating = np.ones(parameter.time_horizon + 1)
        self.plant_efficiency = parameter.plant_efficiency * self.derating

        self.gross_heat_input = self.power_generation / self.plant_efficiency
        display_as(self.gross_heat_input, 'TJ')

        self.coal_used = self.gross_heat_input / parameter.coal.heat_value
        display_as(self.coal_used, 't')

        Emitter.__init__(self,
                         Activity(name=parameter.coal.name,
                                  level=self.coal_used,
                                  emission_factor=parameter.emission_factor[parameter.coal.name]),
                         emission_control=parameter.emission_control)

        self._coal_cost = None

    @property
    def coal_cost(self):
        if self._coal_cost is None:
            raise AttributeError('Accessing  PowerPlant.coal_cost  value before it is set')
        return display_as(self._coal_cost, 'kUSD')

    @coal_cost.setter
    def coal_cost(self, value):
        self._coal_cost = value

    def operating_expenses(self):
        cost = self.fuel_cost() + self.operation_maintenance_cost()
        return display_as(cost, 'kUSD')

    def fuel_cost(self):
        return self.coal_cost

    def operation_maintenance_cost(self):
        return display_as(self.coal_om_cost(), 'kUSD')

    def coal_om_cost(self):
        """Return the vector of operation and maintenance cost."""
        fixed_om_coal = (np.ones(self.parameter.time_horizon + 1) *
                         self.parameter.fix_om_coal * self.parameter.capacity * y)
        variable_om_coal = self.power_generation * self.parameter.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, 'kUSD')

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        """Return the levelized cost of electricity, taxes included."""
        total_lifetime_power_production = npv(discount_rate, self.power_generation)
        total_life_cycle_cost = npv(discount_rate,
                                    self.cash_out(tax_rate, depreciation_period))
        result = total_life_cycle_cost / total_lifetime_power_production
        return display_as(result, 'USD/MWh')

    def coal_transport_tkm(self):
        return self.coal_used * 2 * self.parameter.coal.transport_distance   # Return trip inputed

    def coal_transporter(self):
        """Return an Emitter object to access emissions from coal transport."""
        transport_mean = self.parameter.coal.transport_mean
        activity = Activity(
            name=transport_mean,
            level=self.coal_transport_tkm(),
            emission_factor=self.parameter.emission_factor[transport_mean])
        return Emitter(activity)

    def characteristics(self):
        """Describe the technical characteristics of the plant."""
        description = pd.Series(name=self.parameter.name)
        description["Comissioning year"] = self.parameter.commissioning
        description["Boiler technology"] = self.parameter.boiler_technology
        description["Installed capacity"] = self.parameter.capacity
        description["Capacity factor"] = self.parameter.capacity_factor
        description["Coal consumption"] = self.coal_used[1]
        description["Heat value of coal"] = self.parameter.coal.heat_value
        description["Plant efficiency"] = self.plant_efficiency[1]
        description["Boiler efficiency"] = self.parameter.boiler_efficiency_new
        return description

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = pd.Series(name=self.name)
        statement["Investment    (MUSD)"] = self.capital / MUSD
        statement["Fuel cost     (MUSD)"] = npv(discount_rate, self.fuel_cost()) / MUSD
        statement["  Coal        (MUSD)"] = npv(discount_rate, self.coal_cost) / MUSD
        statement["  Biomass     (MUSD)"] = 0
        statement["O&M cost      (MUSD)"] = npv(
            discount_rate, self.operation_maintenance_cost()) / MUSD
        statement["  O&M coal    (MUSD)"] = npv(
            discount_rate, self.coal_om_cost()) / MUSD
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


class CofiringPlant(PowerPlant):
    """A coal-fired power plant which co-fires biomass."""

    def __init__(self, plant_parameter, cofire_parameter):
        """Initialize the cofiring plant.

        1/ Instanciate as a PowerPlant with a lower efficiency and higher capital cost
        2/ Compute the biomass used and coal saved
        3/ Overwrite the list of activities from grandparent class Emitter.

        The financials (revenue, coal_cost, biomass_cost) are not initialized at this time,
        they must be defined later:

        >>> from manuscript1.parameters import plant_parameter_MD1, cofire_MD1, price_MD1
        >>> plant = CofiringPlant(plant_parameter_MD1, cofire_MD1)
        >>> plant.revenue = plant.power_generation * price_MD1.electricity
        >>> plant.coal_cost = plant.coal_used * price_MD1.coal # free transport in test
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
                              * plant_parameter.coal.heat_value
                              / cofire_parameter.biomass.heat_value)

        boiler_efficiency = (np.ones(plant_parameter.time_horizon + 1) *
                             plant_parameter.boiler_efficiency_new
                             - cofire_parameter.boiler_efficiency_loss(biomass_ratio_mass))
        boiler_efficiency[0] = plant_parameter.boiler_efficiency_new

        PowerPlant.__init__(
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

        self.coal_saved = biomass_heat / plant_parameter.coal.heat_value

        self.coal_used -= self.coal_saved

        self.activities = [
            Activity(
                name=plant_parameter.coal.name,
                level=self.coal_used,
                emission_factor=plant_parameter.emission_factor[plant_parameter.coal.name]),
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

    def fuel_cost(self):
        cost = self.coal_cost + self.biomass_cost
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        cost = self.coal_om_cost() + self.biomass_om_cost()
        return display_as(cost, 'kUSD')

    def coal_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_coal = ((1 - self.cofire_parameter.biomass_ratio_energy)
                         * self.parameter.fix_om_coal
                         * self.parameter.capacity * y)
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = ((1 - self.cofire_parameter.biomass_ratio_energy)
                            * self.power_generation
                            * self.parameter.variable_om_coal)
        cost = fixed_om_coal + variable_om_coal
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
        statement = PowerPlant.lcoe_statement(self, discount_rate, tax_rate, depreciation_period)
        statement["  Biomass     (MUSD)"] = npv(discount_rate, self.biomass_cost) / MUSD
        statement["  O&M biomass (MUSD)"] = npv(discount_rate, self.biomass_om_cost()) / MUSD
        return statement
