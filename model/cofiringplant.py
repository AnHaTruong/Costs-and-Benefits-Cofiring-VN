# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A coal power plant cofiring biomass
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Define a CofiringPlant, subclass of CoalPowerPlant."""

from collections import namedtuple

from pandas import Series, DataFrame, concat

from model.utils import (
    y,
    MUSD,
    display_as,
    safe_divide,
    ones,
    TIME_HORIZON,
    npv,
    after_invest,
)

from model.coalpowerplant import CoalPowerPlant
from model.emitter import Activity


CofiringParameter = namedtuple(
    "CofiringParameter",
    [
        "investment_cost",
        "fix_om_cost",
        "variable_om_cost",
        "OM_hour_MWh",
        "wage_operation_maintenance",
        "cofire_rate",
        "biomass",
        "boiler_efficiency_loss",
    ],
)


# pylint: disable=too-many-instance-attributes
class CofiringPlant(CoalPowerPlant):
    """A coal-fired power plant which co-fires biomass."""

    def __init__(self, plant_parameter, cofire_parameter, emission_factor):
        """Initialize the cofiring plant.

        1/ Instanciate as a CoalPowerPlant with a lower efficiency and higher capital cost
        2/ Compute the biomass used and coal saved
        3/ Overwrite the list of activities from grandparent class Emitter.

        The financials (revenue, coal_cost, biomass_cost) are not initialized at this time,
        they must be defined later.
        """
        self.cofire_parameter = cofire_parameter

        self.biomass_ratio_energy = after_invest(cofire_parameter.cofire_rate)

        biomass_ratio_mass = (
            self.biomass_ratio_energy
            * plant_parameter.coal.heat_value
            / cofire_parameter.biomass.heat_value
        )

        boiler_efficiency = ones(
            TIME_HORIZON + 1
        ) * plant_parameter.boiler_efficiency_new - cofire_parameter.boiler_efficiency_loss(
            biomass_ratio_mass
        )
        boiler_efficiency[0] = plant_parameter.boiler_efficiency_new

        CoalPowerPlant.__init__(
            self,
            plant_parameter,
            emission_factor,
            derating=boiler_efficiency / plant_parameter.boiler_efficiency_new,
            amount_invested=(
                cofire_parameter.investment_cost
                * plant_parameter.capacity
                * cofire_parameter.cofire_rate
            ),
        )

        self.name = plant_parameter.name + " Cofire"

        biomass_heat = self.gross_heat_input * self.biomass_ratio_energy

        self.biomass_used = biomass_heat / cofire_parameter.biomass.heat_value
        display_as(self.biomass_used, "t")

        # Warning: avoided coal at the cofiring plant is not same as ex post - ex ante saved coal
        # because the plant efficiencies differ
        self.coal_used -= biomass_heat / plant_parameter.coal.heat_value

        self.activities = [
            Activity(
                name=plant_parameter.coal.name,
                level=self.coal_used,
                emission_factor=self.emission_factor[plant_parameter.coal.name],
            ),
            Activity(
                name="Straw",
                level=self.biomass_used,
                emission_factor=self.emission_factor[cofire_parameter.biomass.name],
            ),
        ]

        self._biomass_cost = None

    @property
    def biomass_cost(self):
        """Return the cost of biomass.  Decorator @property means it is a getter method."""
        if self._biomass_cost is None:
            raise AttributeError(
                "Accessing  CofiringPlant.biomass_cost  value before it is set"
            )
        return display_as(self._biomass_cost, "kUSD")

    @biomass_cost.setter
    def biomass_cost(self, value):
        self._biomass_cost = value

    def biomass_cost_per_t(self):
        return safe_divide(self.biomass_cost, self.biomass_used)

    def biomass_energy_cost(self):
        cost = self.biomass_cost_per_t() / self.cofire_parameter.biomass.heat_value
        return display_as(cost, "USD / GJ")

    def fuel_cost(self):
        cost = self.coal_cost + self.biomass_cost
        return display_as(cost, "kUSD")

    def operation_maintenance_cost(self):
        cost = self.coal_om_cost() + self.biomass_om_cost()
        return display_as(cost, "kUSD")

    def coal_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_coal = (
            (1 - self.biomass_ratio_energy)
            * self.parameter.fix_om_coal
            * self.parameter.capacity
            * y
        )
        # Variable costs proportional to generation after capacity factor
        variable_om_coal = (
            (1 - self.biomass_ratio_energy)
            * self.power_generation
            * self.parameter.variable_om_coal
        )
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, "kUSD")

        # Approximation "Small biomass ratio"
        # We don't count the lower O&M work for the coal firing parts of the plant.

    def biomass_om_work(self):
        """Return the hours of Operation and Maintenance for the biomass part of the plant."""
        time = (
            self.power_generation
            * self.biomass_ratio_energy
            * self.cofire_parameter.OM_hour_MWh
        )
        return display_as(time, "hr")

    def biomass_om_wages(self):
        amount = (
            self.biomass_om_work() * self.cofire_parameter.wage_operation_maintenance
        )
        return display_as(amount, "kUSD")

    def biomass_om_cost(self):
        """Return  Operation and Maintenance costs of the biomass cofiring part of the plant."""
        fixed_om_bm = (
            self.biomass_ratio_energy
            * self.cofire_parameter.fix_om_cost
            * self.parameter.capacity
            * y
        )
        var_om_bm = (
            self.biomass_ratio_energy
            * self.power_generation
            * self.cofire_parameter.variable_om_cost
        )
        cost = fixed_om_bm + var_om_bm
        # error_message = "Biomass O&M variable costs appear lower than biomass OM wages."
        # assert var_om_bm[1] > self.biomass_om_wages()[1], error_message
        return display_as(cost, "kUSD")

    def operating_expenses_detail(self):
        """Tabulate the annual operating expenses."""
        expenses_data = [
            self.coal_cost,
            self.biomass_cost,
            self.coal_om_cost(),
            self.biomass_om_cost(),
        ]
        expenses_index = [
            "Fuel cost, coal",
            "Fuel cost, biomass",
            "O&M, coal",
            "O&M, biomass",
        ]
        df = DataFrame(data=expenses_data, index=expenses_index)
        df.loc["= Operating expenses"] = df.sum()
        return df

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = CoalPowerPlant.lcoe_statement(
            self, discount_rate, tax_rate, depreciation_period
        )
        statement["  Biomass     (MUSD)"] = npv(discount_rate, self.biomass_cost) / MUSD
        statement["  O&M biomass (MUSD)"] = (
            npv(discount_rate, self.biomass_om_cost()) / MUSD
        )
        return statement

    def parameters_table(self):
        """Tabulate the arguments defining the cofiring plant. Return a Pandas Series."""
        a = CoalPowerPlant.parameters_table(self)
        a["name"] = self.name
        b = Series(self.cofire_parameter, self.cofire_parameter._fields)
        display_as(b.loc["investment_cost"], "USD / kW")
        display_as(b.loc["fix_om_cost"], "USD / kW / y")
        display_as(b.loc["variable_om_cost"], "USD / kWh")
        display_as(b.loc["wage_operation_maintenance"], "USD / hr")
        return concat([a, b])
