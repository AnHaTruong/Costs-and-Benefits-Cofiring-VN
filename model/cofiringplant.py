# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A power plant with cofiring two fuels, for example Coal with Biomass
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Define a CofiringPlant, subclass of PowerPlant."""

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

from model.powerplant import PowerPlant
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
        "cofuel",
        "boiler_efficiency_loss",
    ],
)


# pylint: disable=too-many-instance-attributes
class CofiringPlant(PowerPlant):
    """A flame power plant which co-fires the (main) fuel with a cofuel.

    For example the fuel is coal, the cofuel is biomass.
    """

    def __init__(self, plant_parameter, cofire_parameter, emission_factor):
        """Initialize the cofiring plant.

        1/ Instanciate as a PowerPlant with a lower efficiency and higher capital cost
        2/ Compute the co-fuel used and main fuel saved
        3/ Overwrite the list of activities from grandparent class Emitter.

        The financials (revenue, mainfuel_cost, cofuel_cost) are not initialized at this time,
        they must be defined later.
        """
        self.cofire_parameter = cofire_parameter

        self.cofuel_ratio_energy = after_invest(cofire_parameter.cofire_rate)

        cofuel_ratio_mass = (
            self.cofuel_ratio_energy
            * plant_parameter.fuel.heat_value
            / cofire_parameter.cofuel.heat_value
        )

        boiler_efficiency = ones(
            TIME_HORIZON + 1
        ) * plant_parameter.boiler_efficiency_new - cofire_parameter.boiler_efficiency_loss(
            cofuel_ratio_mass
        )
        boiler_efficiency[0] = plant_parameter.boiler_efficiency_new

        PowerPlant.__init__(
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

        cofuel_heat = self.gross_heat_input * self.cofuel_ratio_energy

        self.cofuel_used = cofuel_heat / cofire_parameter.cofuel.heat_value
        display_as(self.cofuel_used, "t")

        # Warning: avoided fuel (coal) at the cofiring plant is not same as
        # ex post - ex ante  saved fuel because the plant efficiencies differ
        self.mainfuel_used -= cofuel_heat / plant_parameter.fuel.heat_value

        self.activities = [
            Activity(
                name=plant_parameter.fuel.name,
                level=self.mainfuel_used,
                emission_factor=self.emission_factor[plant_parameter.fuel.name],
            ),
            Activity(
                name="Straw",
                level=self.cofuel_used,
                emission_factor=self.emission_factor[cofire_parameter.cofuel.name],
            ),
        ]

        self._cofuel_cost = None

    @property
    def cofuel_cost(self):
        """Return the cost of cofuel.  Decorator @property means it is a getter method."""
        if self._cofuel_cost is None:
            raise AttributeError(
                "Accessing  CofiringPlant.cofuel_cost  value before it is set"
            )
        return display_as(self._cofuel_cost, "kUSD")

    @cofuel_cost.setter
    def cofuel_cost(self, value):
        self._cofuel_cost = value

    def cofuel_cost_per_t(self):
        return safe_divide(self.cofuel_cost, self.cofuel_used)

    def cofuel_energy_cost(self):
        cost = self.cofuel_cost_per_t() / self.cofire_parameter.cofuel.heat_value
        return display_as(cost, "USD / GJ")

    def fuel_cost(self):
        cost = self.mainfuel_cost + self.cofuel_cost
        return display_as(cost, "kUSD")

    def operation_maintenance_cost(self):
        cost = self.mainfuel_om_cost() + self.cofuel_om_cost()
        return display_as(cost, "kUSD")

    def mainfuel_om_cost(self):  # DISCUSS THIS
        # Fixed costs are proportional to capacity
        fixed_om_main = (
            (1 - self.cofuel_ratio_energy)
            * self.parameter.fix_om_main
            * self.parameter.capacity
            * y
        )
        # Variable costs proportional to generation after capacity factor
        variable_om_main = (
            (1 - self.cofuel_ratio_energy)
            * self.power_generation
            * self.parameter.variable_om_main
        )
        cost = fixed_om_main + variable_om_main
        return display_as(cost, "kUSD")

        # Approximation "Small cofuel ratio"
        # We don't count the lower O&M work for the coal firing parts of the plant.

    def cofuel_om_work(self):
        """Return the hours of Operation and Maintenance for the cofuel part of the plant."""
        time = (
            self.power_generation
            * self.cofuel_ratio_energy
            * self.cofire_parameter.OM_hour_MWh
        )
        return display_as(time, "hr")

    def cofuel_om_wages(self):
        amount = (
            self.cofuel_om_work() * self.cofire_parameter.wage_operation_maintenance
        )
        return display_as(amount, "kUSD")

    def cofuel_om_cost(self):
        """Return  Operation and Maintenance costs of the cofuel cofiring part of the plant."""
        fixed_om_bm = (
            self.cofuel_ratio_energy
            * self.cofire_parameter.fix_om_cost
            * self.parameter.capacity
            * y
        )
        var_om_bm = (
            self.cofuel_ratio_energy
            * self.power_generation
            * self.cofire_parameter.variable_om_cost
        )
        cost = fixed_om_bm + var_om_bm
        # error_message = "Cofuel O&M variable costs appear lower than cofuel OM wages."
        # assert var_om_bm[1] > self.cofuel_om_wages()[1], error_message
        return display_as(cost, "kUSD")

    def operating_expenses_detail(self):
        """Tabulate the annual operating expenses."""
        expenses_data = [
            self.mainfuel_cost,
            self.cofuel_cost,
            self.mainfuel_om_cost(),
            self.cofuel_om_cost(),
        ]
        expenses_index = [
            "Fuel cost, main fuel",
            "Fuel cost, cofuel",
            "O&M, main fuel",
            "O&M, cofuel",
        ]
        df = DataFrame(data=expenses_data, index=expenses_index)
        df.loc["= Operating expenses"] = df.sum()
        return df

    def lcoe_statement(self, discount_rate, horizon, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = PowerPlant.lcoe_statement(
            self, discount_rate, horizon, tax_rate, depreciation_period
        )
        statement["  Cofuel      (MUSD)"] = (
            npv(self.cofuel_cost, discount_rate, horizon) / MUSD
        )
        statement["  O&M Cofuel  (MUSD)"] = (
            npv(self.cofuel_om_cost(), discount_rate, horizon) / MUSD
        )
        return statement

    def parameters_table(self):
        """Tabulate the arguments defining the cofiring plant. Return a Pandas Series."""
        a = PowerPlant.parameters_table(self)
        a["name"] = self.name
        b = Series(self.cofire_parameter, self.cofire_parameter._fields)
        display_as(b.loc["investment_cost"], "USD / kW")
        display_as(b.loc["fix_om_cost"], "USD / kW / y")
        display_as(b.loc["variable_om_cost"], "USD / kWh")
        display_as(b.loc["wage_operation_maintenance"], "USD / hr")
        return concat([a, b])
