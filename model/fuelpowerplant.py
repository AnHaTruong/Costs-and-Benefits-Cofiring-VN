# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# A power plant that burns one kind of fuel
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Define FuelPowerPlant, which should be subclassed from PowerPlant.

A flame power plant burns a single fuel to produce electricity.
"""

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
        "fix_om_fuel",
        "variable_om_fuel",
        "emission_control",
        "fuel",
    ],
)


# pylint: disable=too-many-instance-attributes, too-many-arguments
class FuelPowerPlant(Accountholder, Emitter):
    """A flame power plant, burning a single fuel."""

    def __init__(
        self,
        parameter,
        emission_factor,
        time_horizon=TIME_HORIZON,
        derating=None,
        amount_invested=0 * USD,
    ):
        """Initialize the power plant, compute the amount of fuel used.

        The financials (revenue and mainfuel_cost) are not initialized and must be defined later.
        For example:
        a/ instantiate      plant = FuelPowerPlant(plant_parameter_MD1)
        b/ assign           plant.revenue = plant.power_generation * price_MD1.electricity
        c/ assign           plant.mainfuel_cost = plant.mainfuel_used * price_MD1.coal
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

        self.mainfuel_used = self.gross_heat_input / parameter.fuel.heat_value
        display_as(self.mainfuel_used, "t")

        Emitter.__init__(
            self,
            Activity(
                name=parameter.fuel.name,
                level=self.mainfuel_used,
                emission_factor=self.emission_factor[parameter.fuel.name],
            ),
            emission_control=parameter.emission_control,
        )

        self._mainfuel_cost = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.parameter == other.parameter
        return False

    @property
    def mainfuel_cost(self):
        """Return the cost of main fuel. Decorator @property means it is a getter method."""
        if self._mainfuel_cost is None:
            raise AttributeError(
                "Accessing  FuelPowerPlant.mainfuel_cost  value before it is set"
            )
        return display_as(self._mainfuel_cost, "kUSD")

    @mainfuel_cost.setter
    def mainfuel_cost(self, value):
        self._mainfuel_cost = value

    def fuel_cost(self):
        """Return the total fuel cost, not really usefull if only one kind of fuel."""
        return self.mainfuel_cost

    def operating_expenses(self):
        cost = self.fuel_cost() + self.operation_maintenance_cost()
        return display_as(cost, "kUSD")

    def operating_expenses_detail(self):
        """Tabulate the annual operating expenses."""
        expenses_data = [self.fuel_cost(), self.operation_maintenance_cost()]
        expenses_index = ["Fuel cost, main fuel", "Operation & Maintenance"]
        df = DataFrame(data=expenses_data, index=expenses_index)
        df.loc["= Operating expenses"] = df.sum()
        return df

    def operation_maintenance_cost(self):
        return display_as(self.mainfuel_om_cost(), "kUSD")

    def mainfuel_om_cost(self):
        """Return the vector of operation and maintenance cost."""
        fixed_om_fuel = (
            self.ones * self.parameter.fix_om_fuel * self.parameter.capacity * y
        )
        variable_om_fuel = self.power_generation * self.parameter.variable_om_fuel
        cost = fixed_om_fuel + variable_om_fuel
        return display_as(cost, "kUSD")

    def lcoe(self, discount_rate, tax_rate, depreciation_period):
        """Return the levelized cost of electricity, taxes included."""
        total_lifetime_power_production = npv(discount_rate, self.power_generation)
        total_life_cycle_cost = npv(
            discount_rate, self.cash_out(tax_rate, depreciation_period)
        )
        result = total_life_cycle_cost / total_lifetime_power_production
        return display_as(result, "USD/MWh")

    def fuel_transport_tkm(self):
        return (
            self.mainfuel_used * 2 * self.parameter.fuel.transport_distance
        )  # Return trip inputed

    def fuel_reseller(self):
        """Return an Emitter object to access emissions from fuel transport."""
        transport_mean = self.parameter.fuel.transport_mean
        activity = Activity(
            name=transport_mean,
            level=self.fuel_transport_tkm(),
            emission_factor=self.emission_factor[transport_mean],
        )
        return Emitter(activity)

    def parameters_table(self):
        """Tabulate the arguments defining the plant. Return a Pandas Series."""
        set_option("display.max_colwidth", 80)
        a = Series(self.parameter, self.parameter._fields)
        a["derating"] = f"{self.derating[0]}, {self.derating[1]:4f}, ..."
        a["amount_invested"] = self.amount_invested
        display_as(a.loc["fix_om_fuel"], "USD / kW / y")
        display_as(a.loc["variable_om_fuel"], "USD / kWh")
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
        description["Fuel consumption"] = self.mainfuel_used[1]
        description["Fuel type"] = self.parameter.fuel.name
        description["Fuel heat value"] = self.parameter.fuel.heat_value
        description["Fuel transport distance"] = self.parameter.fuel.transport_distance
        description["Fuel transport mean"] = self.parameter.fuel.transport_mean
        return description

    def lcoe_statement(self, discount_rate, tax_rate, depreciation_period):
        """Assess the levelized cost of electricity."""
        statement = Series(name=self.name, dtype=float)
        statement["Investment    (MUSD)"] = self.amount_invested / MUSD
        statement["Fuel cost     (MUSD)"] = npv(discount_rate, self.fuel_cost()) / MUSD
        statement["  Main fuel   (MUSD)"] = (
            npv(discount_rate, self.mainfuel_cost) / MUSD
        )
        statement["  Cofuel      (MUSD)"] = 0
        statement["O&M cost      (MUSD)"] = (
            npv(discount_rate, self.operation_maintenance_cost()) / MUSD
        )
        statement["  O&M Mainfuel(MUSD)"] = (
            npv(discount_rate, self.mainfuel_om_cost()) / MUSD
        )
        statement["  O&M Cofuel  (MUSD)"] = 0
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
