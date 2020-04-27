# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A coal power plant
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Define CoalPowerPlant, which should be subclassed from PowerPlant."""

from collections import namedtuple

from pandas import Series, DataFrame, set_option

from model.utils import (
    y,
    USD,
    MUSD,
    display_as,
    ones,
    TIME_HORIZON,
    npv,
)

# from model.utils import TIME_HORIZON
from model.accountholder import Accountholder
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


# pylint: disable=too-many-instance-attributes, too-many-arguments
class CoalPowerPlant(Accountholder, Emitter):
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
        a/ instantiate      plant = CoalPowerPlant(plant_parameter_MD1)
        b/ assign           plant.revenue = plant.power_generation * price_MD1.electricity
        c/ assign           plant.coal_cost = plant.coal_used * price_MD1.coal
        d/ Now you can      print(plant.net_present_value(discount_rate=0.08))

        The capital cost is left to zero because
        it does not influence results we are interested in this model.
        """
        self.time_horizon = time_horizon
        self.ones = ones(self.time_horizon + 1)

        Accountholder.__init__(self, parameter.name, self.time_horizon, amount_invested)
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
                "Accessing  CoalPowerPlant.coal_cost  value before it is set"
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
        description = Series(name=self.parameter.name, dtype=object)
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
        statement = Series(name=self.name, dtype=float)
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
