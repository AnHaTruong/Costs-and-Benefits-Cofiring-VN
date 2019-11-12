# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2019
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Define the result tables."""

import pandas as pd

# pylint: disable=wrong-import-order
from model.utils import display_as, isclose, USD, kUSD, FTE, year_1
from natu.units import y, t, hr


#%%


def emission_reductions_by_activity(system_a, system_b, external_cost):
    """Summarize the emissions reduction in mass and value."""
    reductions_a = year_1(system_a.emission_reduction(external_cost))
    reductions_b = year_1(system_b.emission_reduction(external_cost))
    contents = [
        reductions_a['Plant'] / (t / y),
        reductions_a['Transport'] / (t / y),
        reductions_a['Field'] / (t / y),
        reductions_b['Plant'] / (t / y),
        reductions_b['Transport'] / (t / y),
        reductions_b['Field'] / (t / y)]
    headers = ["Plant " + system_a.plant.parameter.name, "Transport", "Field",
               "Plant " + system_b.plant.parameter.name, "Transport", "Field"]
    table = pd.DataFrame(
        data=contents,
        index=headers)
    table["Unit"] = ["t/y", "t/y", "t/y", "t/y", "t/y", "t/y"]
    return table[["Unit", "CO2", "SO2", "PM10", "NOx"]]

#%%


def emission_reductions_benefits(system_a, system_b, external_cost):
    """Summarize the emissions reduction in mass and value."""
    reductions_a = year_1(system_a.emission_reduction(external_cost))
    reductions_b = year_1(system_b.emission_reduction(external_cost))
    contents = [
        reductions_a['Total'] / (t / y),
        reductions_a['Relative'] * 100,
        reductions_a['Benefit'] / (kUSD / y),
        reductions_b['Total'] / (t / y),
        reductions_a['Relative'] * 100,
        reductions_b['Benefit'] / (kUSD / y)]
    headers = [" Quantity", "Percent", "Value",
               " Quantity", "Percent", "Value"]
    table = pd.DataFrame(
        data=contents,
        index=headers)
    table["Unit"] = ["t/y", "%", "kUSD/y", "t/y", "%", "kUSD/y"]
    return table[["CO2", "SO2", "PM10", "NOx"]].T


#%%


def emission_reductions(system_a, system_b, external_cost):
    """Summarize the emissions reduction in mass and value."""
    reductions_a = year_1(system_a.emission_reduction(external_cost))
    reductions_b = year_1(system_b.emission_reduction(external_cost))
    contents = [
        external_cost / (USD / t),
        reductions_a['Total'] / (t / y), reductions_a['Benefit'] / (kUSD / y),
        reductions_b['Total'] / (t / y), reductions_b['Benefit'] / (kUSD / y)]
    headers = ['Specific cost',
               " Quantity", "Value",
               " Quantity", "Value"]
    table = pd.DataFrame(
        data=contents,
        index=headers)
    table["Unit"] = ["USD/t", "t/y", "kUSD/y", "t/y", "kUSD/y"]
    return table[["Unit", "CO2", "SO2", "PM10", "NOx"]].T

#%%


def energy_cost(price, fuel):
    """Return the cost per unit of energy contained in the fuel."""
    cost = price / fuel.heat_value
    return display_as(cost, 'USD / GJ')


def energy_costs(system_a, system_b):
    """Tabulate the costs of energy per GJ in different fuels.

    Coal price is defined at plant gate, that is including shipping cost.
    Straw price is defined exogenously as price in field.
    Transport costs are added to know the price at plant gate.
    """
    lines = ["Cost of heat        " + system_a.plant.name + "        " + system_b.plant.name]

    lines.append(
        "Coal                "
        + str(energy_cost(system_a.price.coal, system_a.plant.parameter.coal))
        + "      "
        + str(energy_cost(system_b.price.coal, system_b.plant.parameter.coal)))

    lines.append(
        "Biomass in field    "
        + str(energy_cost(
            system_a.price.biomass_fieldside,
            system_a.cofiring_plant.cofire_parameter.biomass))
        + "      "
        + str(energy_cost(
            system_b.price.biomass_fieldside,
            system_b.cofiring_plant.cofire_parameter.biomass)))

    lines.append(
        "Biomass plant gate  "
        + str(system_a.cofiring_plant.biomass_energy_cost()[1])
        + "      "
        + str(system_b.cofiring_plant.biomass_energy_cost()[1]))

    return '\n'.join(lines)

#%%


def straw_supply(system_a, system_b):
    """Tabulate the straw requires and straw costs."""
    table = [""]

    col3 = system_a.cofiring_plant.biomass_used[1]
    col4 = system_b.cofiring_plant.biomass_used[1]

    col5 = system_a.cofiring_plant.biomass_cost_per_t()[1]
    col6 = system_b.cofiring_plant.biomass_cost_per_t()[1]

    assert isclose(col5, system_a.price.biomass_plantgate), "Problem with price at plant gate"
    assert isclose(col6, system_b.price.biomass_plantgate), "Problem with price at plant gate"

    col9 = system_a.transport_cost_per_t[1]
    col10 = system_b.transport_cost_per_t[1]

    col11 = system_a.price.biomass_fieldside
    col12 = system_b.price.biomass_fieldside
    display_as(col11, "USD/t")
    display_as(col12, "USD/t")

    assert isclose(col11, system_a.farmer.revenue[1] / col3), "Problem with field side price"
    assert isclose(col12, system_b.farmer.revenue[1] / col4), "Problem with field side price"

    table.append('{:24}{:>24}{:>24}'.format('Parameter', system_a.plant.name, system_b.plant.name))
    table.append('{:24} {:>19.0f}{:>22.0f}'.format('Amount required', col3, col4))
    table.append('{:24} {:>22.2f}{:>18.2f}'.format('Cost plant gate', col5, col6))
    table.append('{:24} {:>19.2f}{:>18.2f}'.format('Transportation cost', col9, col10))
    table.append('{:24} {:>22.2f}{:>18.2f}'.format('Cost field side', col11, col12))
    table.append('')
    table.append(system_a.plant.name + ' ' + str(system_a.supply_chain))
    table.append(system_b.plant.name + ' ' + str(system_b.supply_chain))

    return '\n'.join(table)


#%%


def balance_jobs(system_a, system_b):
    """Summarize the implications on jobs created / destroyed."""
    headings = ['Straw collection',
                'Handling',
                'Driving',
                'Plant O & M',
                '- Mining']

    rates = pd.Series(
        data=[system_a.farmer.parameter.wage_bm_collect,
              system_a.transporter.parameter.wage_bm_loading,
              system_a.transporter.parameter.wage_bm_transport,
              system_a.cofiring_plant.cofire_parameter.wage_operation_maintenance,
              system_a.mining_parameter.wage],
        index=headings)

    def work(system):
        return pd.Series(
            data=[system.farmer.labor()[1],
                  system.transporter.loading_work()[1],
                  system.transporter.driving_work()[1],
                  system.cofiring_plant.biomass_om_work()[1],
                  - system.coal_work_lost[1]],
            index=headings)

    def wages(system):
        return pd.Series(
            data=[system.farmer.labor_cost()[1],
                  system.transporter.loading_wages()[1],
                  system.transporter.driving_wages()[1],
                  system.cofiring_plant.biomass_om_wages()[1],
                  - system.coal_wages_lost[1]],
            index=headings)

    contents = [
        rates / (USD / hr),
        work(system_a) / FTE, wages(system_a) / (1000 * USD),
        work(system_b) / FTE, wages(system_b) / (1000 * USD)]
    headers = ["Base salary", "Jobs", "Value",
               "Jobs", "Value"]
    table = pd.DataFrame(
        data=contents,
        index=headers)
    table["= Net change"] = table.sum(axis=1)
    table["Unit"] = ['USD/hr', 'FTE', 'kUSD', 'FTE', 'kUSD']
    return table[["Unit"] + headings + ["= Net change"]].T
