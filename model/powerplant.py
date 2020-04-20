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

from pandas import Series, DataFrame, set_option, concat

from model.utils import (
    y,
    USD,
    MUSD,
    display_as,
    safe_divide,
    ones,
    TIME_HORIZON,
    npv,
    after_invest,
)

# from model.utils import TIME_HORIZON
from model.investment import Investment
from model.emitter import Emitter, Activity


Fuel = namedtuple("Fuel", "name, heat_value, transport_distance, transport_mean")

PlantParameter = namedtuple(
    "PlantParameter",
    [
        "name",
        "capacity",
        "commissioning",
        "boiler_technology",
        "capacity_factor",
        "plant_efficiency",
        "boiler_efficiency_new",
        "fix_om_coal",
        "variable_om_coal",
        "emission_control",
        "coal",
    ],
)

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


# pylint: disable=too-many-instance-attributes, too-many-arguments
class PowerPlant(Investment, Emitter):
    """A coal power plant, without co-firing."""

    def __init__(
        self,
        parameter,
        emission_factor,
        time_horizon=TIME_HORIZON,
        derating=None,
        amount_invested=0 * USD,
    ):
        """Initialize the power plant, compute the amount of coal used.

        The financials (revenue and coal_cost) are not initialized and must be defined later.
        For example:
        a/ instantiate      plant = PowerPlant(plant_parameter_MD1)
        b/ assign           plant.revenue = plant.power_generation * price_MD1.electricity
        c/ assign           plant.coal_cost = plant.coal_used * price_MD1.coal
        d/ Now you can      print(plant.net_present_value(discount_rate=0.08))

        The capital cost represents the cost of installing cofiring,
        it is zero in this case.
        """
        self.time_horizon = time_horizon
        self.ones = ones(self.time_horizon + 1)

        Investment.__init__(self, parameter.name, self.time_horizon, amount_invested)
        self.parameter = parameter
        self.emission_factor = emission_factor

        self.power_generation = (
            self.ones * parameter.capacity * parameter.capacity_factor * y
        )
        display_as(self.power_generation, "GWh")

        if derating is not None:
            self.derating = derating
        else:
            self.derating = self.ones
        self.plant_efficiency = parameter.plant_efficiency * self.derating

        self.gross_heat_input = self.power_generation / self.plant_efficiency
        display_as(self.gross_heat_input, "TJ")

        self.coal_used = self.gross_heat_input / parameter.coal.heat_value
        display_as(self.coal_used, "t")

        Emitter.__init__(
            self,
            Activity(
                name=parameter.coal.name,
                level=self.coal_used,
                emission_factor=self.emission_factor[parameter.coal.name],
            ),
            emission_control=parameter.emission_control,
        )

        self._coal_cost = None

    @property
    def coal_cost(self):
        """Return the cost of coal. Decorator @property means it is a getter method."""
        if self._coal_cost is None:
            raise AttributeError(
                "Accessing  PowerPlant.coal_cost  value before it is set"
            )
        return display_as(self._coal_cost, "kUSD")

    @coal_cost.setter
    def coal_cost(self, value):
        self._coal_cost = value

    def operating_expenses(self):
        cost = self.fuel_cost() + self.operation_maintenance_cost()
        return display_as(cost, "kUSD")

    def operating_expenses_detail(self):
        """Tabulate the annual operating expenses."""
        expenses_data = [self.fuel_cost(), self.operation_maintenance_cost()]
        expenses_index = ["Fuel cost, coal", "Operation & Maintenance"]
        df = DataFrame(data=expenses_data, index=expenses_index)
        df.loc["= Operating expenses"] = df.sum()
        return df

    def fuel_cost(self):
        return self.coal_cost

    def operation_maintenance_cost(self):
        return display_as(self.coal_om_cost(), "kUSD")

    def coal_om_cost(self):
        """Return the vector of operation and maintenance cost."""
        fixed_om_coal = (
            self.ones * self.parameter.fix_om_coal * self.parameter.capacity * y
        )
        variable_om_coal = self.power_generation * self.parameter.variable_om_coal
        cost = fixed_om_coal + variable_om_coal
        return display_as(cost, "kUSD")

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        """Return the levelized cost of electricity, taxes included."""
        total_lifetime_power_production = npv(discount_rate, self.power_generation)
        total_life_cycle_cost = npv(
            discount_rate, self.cash_out(tax_rate, depreciation_period)
        )
        result = total_life_cycle_cost / total_lifetime_power_production
        return display_as(result, "USD/MWh")

    def coal_transport_tkm(self):
        return (
            self.coal_used * 2 * self.parameter.coal.transport_distance
        )  # Return trip inputed

    def coal_reseller(self):
        """Return an Emitter object to access emissions from coal transport."""
        transport_mean = self.parameter.coal.transport_mean
        activity = Activity(
            name=transport_mean,
            level=self.coal_transport_tkm(),
            emission_factor=self.emission_factor[transport_mean],
        )
        return Emitter(activity)

    def parameters_table(self):
        """Tabulate the arguments defining the plant. Return a Pandas Series."""
        set_option("display.max_colwidth", 80)
        a = Series(self.parameter, self.parameter._fields)
        a["derating"] = f"{self.derating[0]}, {self.derating[1]:4f}, ..."
        a["amount_invested"] = self.amount_invested
        display_as(a.loc["fix_om_coal"], "USD / kW / y")
        display_as(a.loc["variable_om_coal"], "USD / kWh")
        display_as(a.loc["amount_invested"], "MUSD")
        return a

    def characteristics(self):
        """Describe the technical characteristics of the plant."""
        # FLAG FOR DELETION.
        #  AFTER UPDATING tests/test_tables.py
        description = Series(name=self.parameter.name)
        description["Comissioning year"] = self.parameter.commissioning
        description["Boiler technology"] = self.parameter.boiler_technology
        description["Installed capacity"] = self.parameter.capacity
        description["Capacity factor"] = self.parameter.capacity_factor
        description["Plant efficiency"] = self.plant_efficiency[1]
        description["Boiler efficiency"] = self.parameter.boiler_efficiency_new
        description["Coal consumption"] = self.coal_used[1]
        description["Coal type"] = self.parameter.coal.name
        description["Coal heat value"] = self.parameter.coal.heat_value
        description["Coal transport distance"] = self.parameter.coal.transport_distance
        description["Coal transport mean"] = self.parameter.coal.transport_mean
        return description

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = Series(name=self.name)
        statement["Investment    (MUSD)"] = self.amount_invested / MUSD
        statement["Fuel cost     (MUSD)"] = npv(discount_rate, self.fuel_cost()) / MUSD
        statement["  Coal        (MUSD)"] = npv(discount_rate, self.coal_cost) / MUSD
        statement["  Biomass     (MUSD)"] = 0
        statement["O&M cost      (MUSD)"] = (
            npv(discount_rate, self.operation_maintenance_cost()) / MUSD
        )
        statement["  O&M coal    (MUSD)"] = (
            npv(discount_rate, self.coal_om_cost()) / MUSD
        )
        statement["  O&M biomass (MUSD)"] = 0
        statement["Tax           (MUSD)"] = (
            npv(discount_rate, self.income_tax(tax_rate, depreciation_period)) / MUSD
        )
        statement["Cash_out      (MUSD)"] = (
            npv(discount_rate, self.cash_out(tax_rate, depreciation_period)) / MUSD
        )
        statement["Electricity produced"] = npv(discount_rate, self.power_generation)
        statement["LCOE                "] = self.lcoe(
            discount_rate, tax_rate, depreciation_period
        )
        return statement


class CofiringPlant(PowerPlant):
    """A coal-fired power plant which co-fires biomass."""

    def __init__(self, plant_parameter, cofire_parameter, emission_factor):
        """Initialize the cofiring plant.

        1/ Instanciate as a PowerPlant with a lower efficiency and higher capital cost
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
        statement = PowerPlant.lcoe_statement(
            self, discount_rate, tax_rate, depreciation_period
        )
        statement["  Biomass     (MUSD)"] = npv(discount_rate, self.biomass_cost) / MUSD
        statement["  O&M biomass (MUSD)"] = (
            npv(discount_rate, self.biomass_om_cost()) / MUSD
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
