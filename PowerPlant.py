# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A Power plant
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#

from natu.numpy import full, npv

from init import time_horizon, v_after_invest, v_ones, display_as, USD, safe_divide
from Investment import Investment
from Emitter import Emitter, Activity


class PowerPlant(Investment, Emitter):
    """ A coal power plant, without co-firing

        The revenue and coal_cost are defined after the initializer:

        >>> from parameters import plant_parameter_MD1, price_MD1
        >>> plant = PowerPlant(plant_parameter_MD1)
        >>> plant.revenue = plant.power_generation * price_MD1.electricity
        >>> plant.coal_cost = plant.coal_used * price_MD1.coal
        >>> print(plant.net_present_value(discount_rate=0.08))
        1.29299e+06 kUSD
    """
    def __init__(self,
                 parameter,
                 derating=v_ones,
                 capital=0 * USD):
        Investment.__init__(self, parameter.name, capital)
        self.parameter = parameter

        self.plant_efficiency = parameter.plant_efficiency * derating

        self.power_generation = full(time_horizon + 1,
                                     parameter.capacity * parameter.capacity_factor,
                                     dtype=object)
        display_as(self.power_generation, 'GWh')

        self.gross_heat_input = self.power_generation / self.plant_efficiency
        display_as(self.gross_heat_input, 'TJ')

        self.coal_used = self.gross_heat_input / parameter.coal.heat_value
        display_as(self.coal_used, 't')

        coal_name = parameter.coal.name
        Emitter.__init__(self,
                         Activity(name=coal_name,
                                  level=self.coal_used,
                                  emission_factor=parameter.emission_factor[coal_name]),
                         emission_control=parameter.emission_control)

        self._coal_cost = None

    @property
    def coal_cost(self):
        if self._coal_cost is None:
            raise AttributeError('Using  PowerPlant.coal_cost  value before it is set')
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
        fixed_om_coal = full(time_horizon + 1,
                             self.parameter.fix_om_coal * self.parameter.capacity,
                             dtype=object)
        variable_om_coal = self.power_generation * self.parameter.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, 'kUSD')

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        total_lifetime_power_production = npv(discount_rate, self.power_generation)
        total_life_cycle_cost = npv(discount_rate,
                                    self.cash_out(tax_rate, depreciation_period))
        result = total_life_cycle_cost / total_lifetime_power_production
        return display_as(result, 'USD/MWh')

    def coal_transport_tkm(self):
        return self.coal_used * 2 * self.parameter.coal.transport_distance   # Return trip inputed

    def coal_transporter(self):
        transport_mean = self.parameter.coal.transport_mean
        activity = Activity(
            name=transport_mean,
            level=self.coal_transport_tkm(),
            emission_factor=self.parameter.emission_factor[transport_mean])
        return Emitter(activity)


# pylint: disable=too-many-instance-attributes
class CofiringPlant(PowerPlant):

    def __init__(self, plant_parameter, cofire_parameter):
        self.cofire_parameter = cofire_parameter

        biomass_ratio_mass = (cofire_parameter.biomass_ratio_energy
                              * plant_parameter.coal.heat_value
                              / cofire_parameter.biomass.heat_value)

        boiler_efficiency = (plant_parameter.boiler_efficiency
                             - cofire_parameter.boiler_efficiency_loss(biomass_ratio_mass))
        boiler_efficiency[0] = plant_parameter.boiler_efficiency[0]

        derating = boiler_efficiency / plant_parameter.boiler_efficiency

        investment_cost = (cofire_parameter.capital_cost
                           * plant_parameter.capacity
                           * float(cofire_parameter.biomass_ratio_energy[1]))

        PowerPlant.__init__(self,
                            plant_parameter,
                            derating,
                            investment_cost)

        self.name = plant_parameter.name + ' Cofire'

        biomass_heat = (v_after_invest
                        * self.gross_heat_input
                        * self.cofire_parameter.biomass_ratio_energy)

        self.biomass_used = biomass_heat / cofire_parameter.biomass.heat_value
        display_as(self.biomass_used, 't')

        self.coal_saved = biomass_heat / plant_parameter.coal.heat_value

        self.coal_used -= self.coal_saved
        coal_name = plant_parameter.coal.name
        biomass_name = cofire_parameter.biomass.name

        self.activities = [Activity(name=coal_name,
                                    level=self.coal_used,
                                    emission_factor=plant_parameter.emission_factor[coal_name]),
                           Activity(name='Straw',
                                    level=self.biomass_used,
                                    emission_factor=plant_parameter.emission_factor[biomass_name])]

        self._biomass_cost = None

    @property
    def biomass_cost(self):
        if self._biomass_cost is None:
            raise AttributeError('Using  CofiringPlant.biomass_cost  value before it is set')
        return display_as(self._biomass_cost, 'kUSD')

    @biomass_cost.setter
    def biomass_cost(self, value):
        self._biomass_cost = value

    def biomass_cost_per_t(self):
        return safe_divide(self.biomass_cost, self.biomass_used)

    def biomass_cost_per_GJ(self):
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
        fixed_om_coal = (v_after_invest
                         * self.parameter.fix_om_coal
                         * self.parameter.capacity
                         * (1 - self.cofire_parameter.biomass_ratio_energy))
        fixed_om_coal[0] = self.parameter.fix_om_coal * self.parameter.capacity
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = (self.power_generation
                            * self.parameter.variable_om_coal
                            * (1 - self.cofire_parameter.biomass_ratio_energy))
        variable_om_coal[0] = self.power_generation[0] * self.parameter.variable_om_coal
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
        fixed_om_bm = (v_after_invest
                       * self.cofire_parameter.fix_om_cost
                       * self.parameter.capacity * self.cofire_parameter.biomass_ratio_energy)
        var_om_bm = (v_after_invest
                     * self.power_generation
                     * self.cofire_parameter.variable_om_cost
                     * self.cofire_parameter.biomass_ratio_energy)
        cost = fixed_om_bm + var_om_bm
        return display_as(cost, 'kUSD')
