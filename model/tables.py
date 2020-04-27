# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2019
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Define result tables, showing two systems at a time.

Methods defined in class System we return complete time series (21 years).

Functions defined here summarize the vectors.
Since we have steady state after year 1, all series matching pattern   s = (a, b, b, b, ..., b)
are better shown as   (a, b, npv(s))
"""

from pandas import DataFrame, Series, concat

# pylint: disable=wrong-import-order
from model.utils import display_as, isclose, y, t, hr, USD, FTE, year_1, summarize
from model.wtawtp import feasibility_by_solving, feasibility_direct


#%%


def emission_reductions_by_activity(system_a, system_b):
    """Summarize the emissions reduction in mass."""
    reductions_a = year_1(system_a.emissions_reduction())
    reductions_b = year_1(system_b.emissions_reduction())
    contents = [
        reductions_a["Plant"] / (t / y),
        reductions_a["Transport"] / (t / y),
        reductions_a["Field"] / (t / y),
        reductions_b["Plant"] / (t / y),
        reductions_b["Transport"] / (t / y),
        reductions_b["Field"] / (t / y),
    ]
    headers = [
        "Plant " + system_a.plant.parameter.name,
        "Transport",
        "Field",
        "Plant " + system_b.plant.parameter.name,
        "Transport",
        "Field",
    ]
    table = DataFrame(data=contents, index=headers)
    table["Unit"] = ["t/y", "t/y", "t/y", "t/y", "t/y", "t/y"]
    return table[["Unit", "CO2", "SO2", "PM10", "NOx"]]


#%%


def emissions_reduction_benefit(system_a, system_b, external_cost, discount_rate):
    """Tabulate the external value of emissions reduction.

    Summarize the time series as [x0, x1, npv(x0, x1, ...)].
    """
    reductions_a = system_a.emissions_reduction_benefit(external_cost)
    reductions_b = system_b.emissions_reduction_benefit(external_cost)
    contents = [
        reductions_a.loc["Reduction"],
        reductions_a.loc["Value"],
        reductions_b.loc["Reduction"],
        reductions_b.loc["Value"],
    ]
    headers = [" Quantity", "Value", " Quantity", "Value"]
    table = DataFrame(data=contents, index=headers)
    table = table.applymap(lambda x: summarize(x, discount_rate))
    return table[["CO2", "SO2", "PM10", "NOx"]].T


def coal_saved_benefit(system_a, system_b, coal_import_price, discount_rate):
    """Tabulate the external value of coal use reduction.

    Summarize the time series as [x0, x1, npv(x0, x1, ...)].
    """
    cols = ["Reduction", "Value"]
    data_a = system_a.coal_saved_benefits(coal_import_price).loc[cols]
    data_a = data_a.apply(lambda x: summarize(x, discount_rate), axis=1)
    data_b = system_b.coal_saved_benefits(coal_import_price).loc[cols]
    data_b = data_b.apply(lambda x: summarize(x, discount_rate), axis=1)
    index = [system_a.plant.name, system_b.plant.name]
    df = DataFrame([data_a, data_b], index=index)
    return df.T


#%%


def emissions_reduction_ICERE(system_a, system_b, external_cost):
    """Tabulate emission reductions amount and value in year 1."""
    table = emissions_reduction_benefit(
        system_a, system_b, external_cost, discount_rate=0
    )
    table = table.applymap(lambda sequence: sequence[1])
    table.insert(loc=0, column="Specific cost", value=external_cost)
    return table


#%%


def energy_cost(price, fuel):
    """Return the cost per unit of energy contained in the fuel."""
    cost = price / fuel.heat_value
    return display_as(cost, "USD / GJ")


def energy_costs(system_a, system_b):
    """Tabulate the costs of energy per GJ in different fuels.

    Coal price is defined at plant gate, that is including shipping cost.
    Straw price is defined exogenously as price in field.
    Transport costs are added to know the price at plant gate.
    """
    lines = [
        "Cost of heat        " + system_a.plant.name + "        " + system_b.plant.name
    ]

    lines.append(
        "Coal                "
        + str(energy_cost(system_a.price.coal, system_a.plant.parameter.fuel))
        + "      "
        + str(energy_cost(system_b.price.coal, system_b.plant.parameter.fuel))
    )

    lines.append(
        "Biomass in field    "
        + str(
            energy_cost(
                system_a.price.biomass_fieldside,
                system_a.cofiring_plant.cofire_parameter.cofuel,
            )
        )
        + "      "
        + str(
            energy_cost(
                system_b.price.biomass_fieldside,
                system_b.cofiring_plant.cofire_parameter.cofuel,
            )
        )
    )

    lines.append(
        "Biomass plant gate  "
        + str(system_a.cofiring_plant.cofuel_energy_cost()[1])
        + "      "
        + str(system_b.cofiring_plant.cofuel_energy_cost()[1])
    )

    return "\n".join(lines)


#%%


def straw_supply(system_a, system_b):
    """Tabulate the straw requires and straw costs."""
    table = [""]

    col3 = system_a.quantity_fieldside[1]
    col4 = system_b.quantity_fieldside[1]

    col5 = system_a.cofiring_plant.cofuel_cost_per_t()[1]
    col6 = system_b.cofiring_plant.cofuel_cost_per_t()[1]

    assert isclose(
        col5, system_a.price.biomass_plantgate
    ), "Problem with price at plant gate"
    assert isclose(
        col6, system_b.price.biomass_plantgate
    ), "Problem with price at plant gate"

    col9 = system_a.transport_cost_per_t[1]
    col10 = system_b.transport_cost_per_t[1]

    col11 = system_a.price.biomass_fieldside
    col12 = system_b.price.biomass_fieldside
    display_as(col11, "USD/t")
    display_as(col12, "USD/t")

    assert isclose(
        col11, system_a.farmer.revenue[1] / col3
    ), "Problem with field side price"
    assert isclose(
        col12, system_b.farmer.revenue[1] / col4
    ), "Problem with field side price"

    table.append(
        "{:24}{:>24}{:>24}".format(
            "Parameter", system_a.plant.name, system_b.plant.name
        )
    )
    table.append("{:24} {:>19.0f}{:>22.0f}".format("Amount required", col3, col4))
    table.append("{:24} {:>22.2f}{:>18.2f}".format("Cost plant gate", col5, col6))
    table.append("{:24} {:>19.2f}{:>18.2f}".format("Transportation cost", col9, col10))
    table.append("{:24} {:>22.2f}{:>18.2f}".format("Cost field side", col11, col12))
    table.append("")
    table.append(system_a.plant.name + " " + str(system_a.supply_chain))
    table.append(system_b.plant.name + " " + str(system_b.supply_chain))

    return "\n".join(table)


#%%


def balance_jobs(system_a, system_b):
    """Summarize the implications on jobs created / destroyed."""
    headings = ["Straw collection", "Handling", "Driving", "Plant O & M", "- Mining"]

    rates = Series(
        data=[
            system_a.farmer.parameter.wage_bm_collect,
            system_a.reseller.parameter.wage_bm_loading,
            system_a.reseller.parameter.wage_bm_transport,
            system_a.cofiring_plant.cofire_parameter.wage_operation_maintenance,
            system_a.mining_parameter.wage_mining,
        ],
        index=headings,
    )

    def work(system):
        return Series(
            data=[
                system.farmer.labor()[1],
                system.reseller.loading_work()[1],
                system.reseller.driving_work()[1],
                system.cofiring_plant.cofuel_om_work()[1],
                -system.coal_work_lost[1],
            ],
            index=headings,
        )

    def wages(system):
        return Series(
            data=[
                system.farmer.labor_cost()[1],
                system.reseller.loading_wages()[1],
                system.reseller.driving_wages()[1],
                system.cofiring_plant.cofuel_om_wages()[1],
                -system.coal_wages_lost[1],
            ],
            index=headings,
        )

    contents = [
        rates / (USD / hr),
        work(system_a) / FTE,
        wages(system_a) / (1000 * USD),
        work(system_b) / FTE,
        wages(system_b) / (1000 * USD),
    ]
    headers = ["Base salary", "Jobs", "Value", "Jobs", "Value"]
    table = DataFrame(data=contents, index=headers)
    table["= Net change"] = table.sum(axis=1)
    table["Unit"] = ["USD/hr", "FTE", "kUSD", "FTE", "kUSD"]
    return table[["Unit"] + headings + ["= Net change"]].T


#%%


def business_value_by_solving(system_a, system_b, discount_rate):
    """Tabulate the WTA and WTP, using the micro definition: call code solving Profit(p) == 0."""
    return concat(
        [
            feasibility_by_solving(system_a, discount_rate),
            feasibility_by_solving(system_b, discount_rate),
        ],
        axis=1,
    )


def business_value_direct(system_a, system_b, discount_rate):
    """Tabulate the feasibility, using the theoretical analysis."""
    return concat(
        [
            feasibility_direct(system_a, discount_rate),
            feasibility_direct(system_b, discount_rate),
        ],
        axis=1,
    )
