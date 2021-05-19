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

from model.utils import kUSD, npv, display_as

#%% Business value in table

row_labels = [
    "Farmer expenses",
    "Reseller expenses",
    "Plant investment",
    "Plant extra O&M",
    "Coal saving",
    "Business value of cofiring",
    "Biomass used total",
    "Biomass used per year",
    "Business value per year",
]

def feasibility_direct(system, discount_rate):
    """Tabulate the feasibility, using the theoretical analysis."""

    wta =  npv(discount_rate, system.farmer.operating_expenses())

    minimum_margin = npv(discount_rate, system.reseller.operating_expenses())

    investment = npv(discount_rate, system.cofiring_plant.investment())

    table_opex = system.plant_npv_opex_change(discount_rate)
    extra_OM = (table_opex.loc["O&M, main fuel"] + table_opex.loc["O&M, cofuel"] )
    
    coal_saving = npv(discount_rate, system.coal_saved * system.price.coal)

    value = coal_saving - extra_OM - investment - wta - minimum_margin

    q = npv(discount_rate, system.farmer.quantity)

    q_per_year = system.quantity_plantgate[1]
 
    potential_per_year = q_per_year / q * value

    data = [
        display_as(wta, "kUSD"),
        display_as(minimum_margin, "kUSD"),
        display_as(investment, "kUSD"),
        display_as(extra_OM, "kUSD"),
        display_as(coal_saving, "kUSD"),
        display_as(value, "kUSD"),
        q,
        q_per_year,
        display_as(potential_per_year, "kUSD"),
    ]

    return Series(data, index=row_labels, name=system.plant.name + " table")


table_MD1 = feasibility_direct(MongDuong1System, discount_rate)
table_NB = feasibility_direct(NinhBinhSystem, discount_rate)

print("From the table, total NPV with discount rate =", discount_rate,":")
print(concat([table_MD1, table_NB], axis=1))


def feasibility_direct_y1(system):
    """Tabulate the feasibility, undiscounted."""

    wta = system.farmer.operating_expenses()[1]
    
    minimum_margin = system.reseller.operating_expenses()[1]

# Suspect the  cause of the difference is amortization
    investment = system.cofiring_plant.investment()[1]

# FIXME: Cut and paste code for year 1
    table_opex = system.plant_npv_opex_change(discount_rate)
    extra_OM = (table_opex.loc["O&M, main fuel"] + table_opex.loc["O&M, cofuel"] )
    
    coal_saving = system.coal_saved[1] * system.price.coal

    print(wta, minimum_margin, investment, extra_OM, coal_saving)

    value = coal_saving - extra_OM - investment - wta - minimum_margin

    q = npv(discount_rate, system.farmer.quantity)

    q_per_year = system.quantity_plantgate[1]
 
    potential_per_year = q_per_year / q * value

    data = [
        display_as(wta, "kUSD"),
        display_as(minimum_margin, "kUSD"),
        display_as(investment, "kUSD"),
        display_as(extra_OM, "kUSD"),
        display_as(coal_saving, "kUSD"),
        display_as(value, "kUSD"),
        q,
        q_per_year,
        display_as(potential_per_year, "kUSD"),
    ]

    return Series(data, index=row_labels, name=system.plant.name + " table")


print("\nFrom the table, year 1:")
table_MD1 = feasibility_direct_y1(MongDuong1System)
table_NB = feasibility_direct_y1(NinhBinhSystem)

print(concat([table_MD1, table_NB], axis=1))

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

    data =  [
            system.farmer.operating_expenses()[1] / kUSD,
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