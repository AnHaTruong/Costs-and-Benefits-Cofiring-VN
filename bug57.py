#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal reproduction for bug 57.

Created on Wed May 19 11:42:09 2021

@author: haduong
"""

from pandas import concat, Series

from manuscript1.parameters import (
    MongDuong1System,
    NinhBinhSystem,
    discount_rate,
    depreciation_period,
)

from model.utils import kUSD, npv, display_as, TIME_HORIZON

#%% Business value in table

row_labels = [
    "Farmer expenses",
    "Reseller expenses",
    "Plant investment",
    "Plant extra O&M",
    "Coal saving",
    "Business value of cofiring",
    "Annual business value of cofiring, levelized",
    "Annual business value of cofiring, linearized"
]


def table2(system, discount_rate, horizon=(TIME_HORIZON + 1)):
    """Tabulate the feasibility, using the theoretical analysis.

    Keeping only  horizon  time periods. Investment in period 0, payback starts at 1
    """

    mask = [1] * horizon + [0] * (TIME_HORIZON + 1 - horizon)

    cost_collect = npv(discount_rate, system.farmer.operating_expenses() * mask)

    minimum_margin = npv(discount_rate, system.reseller.operating_expenses() * mask)

    investment = npv(discount_rate, system.cofiring_plant.investment() * mask)

    extra_OM = npv(discount_rate, system.plant_om_change() * mask)

    coal_saving = npv(discount_rate, system.coal_saved * mask * system.price.coal)

    value = coal_saving - extra_OM - investment - cost_collect - minimum_margin

    value_levelized = value / npv(discount_rate, mask)

    value_linearized = value / (horizon - 1)

    data = [
        display_as(cost_collect, "kUSD"),
        display_as(minimum_margin, "kUSD"),
        display_as(investment, "kUSD"),
        display_as(extra_OM, "kUSD"),
        display_as(coal_saving, "kUSD"),
        display_as(value, "kUSD"),
        display_as(value_levelized, "kUSD"),
        display_as(value_linearized, "kUSD"),
    ]

    result = Series(data, index=row_labels, name=system.plant.name + " table")

    print("Table 2", system.plant.name, "discounted over", horizon, "years at", discount_rate)
    print(result)
    print()


table2(MongDuong1System, discount_rate)
table2(MongDuong1System, 0)
table2(MongDuong1System, 0, 11)


#%% Per ton

row_labels = [
    "Farmer wta",
    "Reseller average cost",
    "Plant investment",
    "Plant extra O&M",
    "Coal saving",
    "Plant wtp",
    "Potential surplus",
    "Biomass used discounted sum",
    "Value of cofiring",
    "Biomass used per year",
    "Business value per year",
]


def table3(system, discount_rate, horizon=(TIME_HORIZON + 1)):
    """Tabulate the feasibility, using the theoretical analysis."""

    mask = [1] * horizon + [0] * (TIME_HORIZON + 1 - horizon)

    q = npv(discount_rate, system.farmer.quantity * mask)

    wta = npv(discount_rate, system.farmer.operating_expenses() * mask) / q

    minimum_margin = npv(discount_rate, system.reseller.operating_expenses() * mask) / q

    investment = npv(discount_rate, system.cofiring_plant.investment() * mask) / q

    extra_OM = npv(discount_rate, system.plant_om_change() * mask) / q

    coal_saving = npv(discount_rate, system.coal_saved * mask * system.price.coal) / q

    wtp = coal_saving - extra_OM - investment

    surplus = wtp - wta - minimum_margin

    q_per_year = system.farmer.quantity[1]

    potential_per_year = q_per_year * surplus

    data = [
        display_as(wta, "USD / t"),
        display_as(minimum_margin, "USD / t"),
        display_as(investment, "USD / t"),
        display_as(extra_OM, "USD / t"),
        display_as(coal_saving, "USD / t"),
        display_as(wtp, "USD / t"),
        display_as(surplus, "USD / t"),
        display_as(q, "kt"),
        display_as(surplus * q, "MUSD"),
        display_as(q_per_year, "kt"),
        display_as(potential_per_year, "kUSD"),
    ]

    result = Series(data, index=row_labels, name=system.plant.name + " table")

    print("Table 3", system.plant.name, "discounted over", horizon, "years at", discount_rate)
    print(result)
    print()


table3(MongDuong1System, discount_rate)
table3(MongDuong1System, 0)
table3(MongDuong1System, 0, 11)  # The one to use


#%% Business value in figure


row_labels2 = [
    "Farmer expenses",
    "Reseller expenses",
    "Plant investment amortization",
    "Plant extra O&M",
    "Total costs",
    "Fuel saved",
    "Business value",
]


def cba(system):
    """Print costs and benefits of cofiring used for the figure."""
    #%% Costs
    extra_om = (
        system.cofiring_plant.operating_expenses_detail().loc["O&M, main fuel"]
        + system.cofiring_plant.operating_expenses_detail().loc["O&M, cofuel"]
        - system.plant.operating_expenses_detail().loc["Operation & Maintenance"]
    )

    data = [system.farmer.operating_expenses()[1] / kUSD,
            system.reseller.operating_expenses()[1] / kUSD,
            system.cofiring_plant.amortization(depreciation_period)[1] / kUSD,
            extra_om[1] / kUSD,
            ]

    total_costs = sum(data)
    data.append(total_costs)

    #%% Benefits

    fuel_saved = (
        system.plant.operating_expenses_detail().loc["Fuel cost, main fuel"]
        - system.cofiring_plant.operating_expenses_detail().loc["Fuel cost, main fuel"]
    )

    data.append(fuel_saved[1])

    #%% Business value

    business_value = fuel_saved[1] / kUSD - total_costs
    data.append(business_value)
    return Series(data, index=row_labels2, name=system.plant.name + " fig")


print("\nFrom the figure, year 1 cash flows:")

print(concat([cba(MongDuong1System), cba(NinhBinhSystem)], axis=1))
