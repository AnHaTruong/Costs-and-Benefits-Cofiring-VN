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

from natu.numpy import full, npv, errstate

from init import time_horizon, v_after_invest, display_as, USD
from Investment import Investment
from Emitter import Emitter


class PowerPlant(Investment, Emitter):
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
                 emission_factor,
                 emission_control,
                 coal,
                 capital=0 * USD
                 ):
        Investment.__init__(self, capital)
        self.name = name
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.plant_efficiency = plant_efficiency
        self.boiler_efficiency = boiler_efficiency
        self.fix_om_coal = fix_om_coal
        self.variable_om_coal = variable_om_coal
#        self.emission_control = emission_control
#        self.emission_factor = emission_factor
        self.coal = coal

        self.power_generation = full(time_horizon + 1,
                                     capacity * capacity_factor,
                                     dtype=object)
        display_as(self.power_generation, 'GWh')

        self.gross_heat_input = self.power_generation / plant_efficiency
        display_as(self.gross_heat_input, 'TJ')

        self.coal_used = self.gross_heat_input / coal.heat_value
        display_as(self.coal_used, 't')

        Emitter.__init__(self,
                         {self.coal.name: self.coal_used},
                         emission_factor,
                         emission_control)
#        self.stack = Emitter({self.coal.name: self.coal_used},
#                             self.emission_factor,
#                             self.emission_control)

    def revenue(self, feedin_tariff):                       # pylint: disable=arguments-differ
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


class CofiringPlant(PowerPlant):

    def __init__(self, plant: PowerPlant, cofire_tech):

        self.plant = plant
        self.biomass_ratio_energy = cofire_tech.biomass_ratio_energy
        self.capital_cost = cofire_tech.capital_cost
        self.fix_om_cost = cofire_tech.fix_om_cost
        self.variable_om_cost = cofire_tech.variable_om_cost
        self.biomass = cofire_tech.biomass
        self.OM_hour_MWh = cofire_tech.OM_hour_MWh
        self.wage_operation_maintenance = cofire_tech.wage_operation_maintenance

        biomass_ratio_mass = (cofire_tech.biomass_ratio_energy
                              * plant.coal.heat_value / self.biomass.heat_value)

        cofiring_boiler_efficiency = (plant.boiler_efficiency
                                      - cofire_tech.boiler_efficiency_loss(biomass_ratio_mass))
        cofiring_boiler_efficiency[0] = plant.boiler_efficiency[0]

        cofiring_plant_efficiency = (plant.plant_efficiency
                                     * cofiring_boiler_efficiency / plant.boiler_efficiency)
        cofiring_plant_efficiency[0] = plant.plant_efficiency[0]

        PowerPlant.__init__(self,
                            plant.name + " Cofire",
                            plant.capacity,
                            plant.capacity_factor,
                            plant.commissioning,
                            plant.boiler_technology,
                            cofiring_plant_efficiency,
                            cofiring_boiler_efficiency,
                            plant.fix_om_coal,
                            plant.variable_om_coal,
                            plant.emission_factor,
                            plant.emission_control,
                            plant.coal,
                            (cofire_tech.capital_cost
                             * plant.capacity
                             * float(cofire_tech.biomass_ratio_energy[1])))

        self.biomass_heat = v_after_invest * self.gross_heat_input * self.biomass_ratio_energy
        display_as(self.biomass_heat, 'TJ')

        self.biomass_used = self.biomass_heat / self.biomass.heat_value
        display_as(self.biomass_used, 't')

        self.coal_saved = self.biomass_heat / plant.coal.heat_value
        display_as(self.coal_saved, 't')

        self.coal_used = (self.gross_heat_input - self.biomass_heat) / self.coal.heat_value
        display_as(self.coal_used, 't')

        Emitter.__init__(self,
                         {self.coal.name: self.coal_used,
                          self.biomass.name: self.biomass_used},
                         plant.emission_factor,
                         plant.emission_control)

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
        with errstate(divide='ignore', invalid='ignore'):
            cost_per_t = self.biomass_cost / self.biomass_used
        return display_as(cost_per_t, 'USD/t')

    def biomass_cost_per_GJ(self):
        cost = self.biomass_cost_per_t() / self.biomass.heat_value
        return display_as(cost, 'USD / GJ')

    def fuel_cost(self):
        cost = self.coal_cost() + self.biomass_cost
        return display_as(cost, 'kUSD')

    def operation_maintenance_cost(self):
        cost = self.coal_om_cost() + self.biomass_om_cost()
        return display_as(cost, 'kUSD')

    def coal_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_coal = (v_after_invest
                         * self.fix_om_coal
                         * self.capacity
                         * (1 - self.biomass_ratio_energy))
        fixed_om_coal[0] = self.fix_om_coal * self.capacity
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = (self.power_generation
                            * self.variable_om_coal
                            * (1 - self.biomass_ratio_energy))
        variable_om_coal[0] = self.power_generation[0] * self.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, 'kUSD')

        # Approximation "Small biomass ratio"
        # We don't count the lower O&M work for the coal firing parts of the plant.
    def biomass_om_work(self):
        time = self.power_generation * self.biomass_ratio_energy * self.OM_hour_MWh
        return display_as(time, 'hr')

    def biomass_om_wages(self):
        amount = self.biomass_om_work() * self.wage_operation_maintenance
        return display_as(amount, 'kUSD')

    def biomass_om_cost(self):
        fixed_om_bm = (v_after_invest
                       * self.fix_om_cost
                       * self.capacity * self.biomass_ratio_energy)
        var_om_bm = (v_after_invest
                     * self.power_generation
                     * self.variable_om_cost
                     * self.biomass_ratio_energy)
        cost = fixed_om_bm + var_om_bm
        return display_as(cost, 'kUSD')

    def coal_saved_cost(self):
        cost = self.coal_saved * self.coal.price
        return display_as(cost, 'kUSD')

    def coal_work_lost(self, mining_productivity):
        time = self.coal_saved / mining_productivity
        return time
