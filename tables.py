# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Define the result tables."""

import pandas as pd

from natu.units import y, t

from model.utils import display_as, isclose, USD, kUSD, FTE, year_1
from parameters import mining_parameter


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
    headers = ["Plant", "Transport", "Field",
               "Plant", "Transport", "Field"]
    df = pd.DataFrame(
        data=contents,
        index=headers)
    df["Unit"] = ["t/y", "t/y", "t/y", "t/y", "t/y", "t/y"]
    return df[["Unit", "CO2", "SO2", "PM10", "NOx"]]

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
    df = pd.DataFrame(
        data=contents,
        index=headers)
    df["Unit"] = ["t/y", "%", "kUSD/y", "t/y", "%", "kUSD/y"]
    return df[["CO2", "SO2", "PM10", "NOx"]].T


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
    df = pd.DataFrame(
        data=contents,
        index=headers)
    df["Unit"] = ["USD/t", "t/y", "kUSD/y", "t/y", "kUSD/y"]
    return df[["Unit", "CO2", "SO2", "PM10", "NOx"]].T

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
            system_a.price.biomass,
            system_a.cofiring_plant.cofire_parameter.biomass))
        + "      "
        + str(energy_cost(
            system_b.price.biomass,
            system_a.cofiring_plant.cofire_parameter.biomass)))

    lines.append(
        "Biomass plant gate  "
        + str(system_a.cofiring_plant.biomass_energy_cost()[1])
        + "      "
        + str(system_b.cofiring_plant.biomass_energy_cost()[1]))

    return '\n'.join(lines)


def straw_supply(system_a, system_b):
    """Tabulate the straw requires and straw costs."""
    table = ["\nTable 5. Straw required and straw cost estimation\n"]

    col3 = system_a.cofiring_plant.biomass_used[1]
    col4 = system_b.cofiring_plant.biomass_used[1]

    col5 = system_a.cofiring_plant.biomass_cost_per_t()[1]
    col6 = system_b.cofiring_plant.biomass_cost_per_t()[1]

    col9 = system_a.transport_cost_per_t[1]
    col10 = system_b.transport_cost_per_t[1]

    assert isclose(col5 - col9, system_a.biomass_value[1] / col3)
    assert isclose(col6 - col10, system_b.biomass_value[1] / col4)

    table.append('{:24}{:>24}{:>24}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))
    table.append('{:24} {:>19.0f}{:>22.0f}'.format('Straw required', col3, col4))
    table.append('{:24} {:>22.2f}{:>18.2f}'.format('Straw cost', col5, col6))
    table.append('{:24} {:>22.2f}{:>18.2f}'.format('Biomass raw cost', col5 - col9, col6 - col10))
    table.append('{:24} {:>19.2f}{:>18.2f}'.format('Biomass transportation cost', col9, col10))
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

    def work(system):
        return pd.Series(
            data=[system.farmer.labor()[1],
                  system.transporter.loading_work()[1],
                  system.transporter.driving_work()[1],
                  system.cofiring_plant.biomass_om_work()[1],
                  - system.coal_work_lost(mining_parameter['productivity_underground'])[1]],
            index=headings)

    def wages(system):
        return pd.Series(
            data=[system.farmer.labor_cost()[1],
                  system.transporter.loading_wages()[1],
                  system.transporter.driving_wages()[1],
                  system.cofiring_plant.biomass_om_wages()[1],
                  - system.coal_work_lost_value(
                      mining_parameter['productivity_underground'],
                      mining_parameter['wage'])[1]],
            index=headings)

    contents = [
        wages(system_a) / (1000 * USD), work(system_a) / FTE,
        wages(system_b) / (1000 * USD), work(system_b) / FTE]
    headers = ["Value", "Jobs",
               "Value", "Jobs"]
    df = pd.DataFrame(
        data=contents,
        index=headers)
    df["= Net change"] = df.sum(axis=1)
    df["Unit"] = ['kUSD', 'FTE', 'kUSD', 'FTE']
    return df[["Unit"] + headings + ["= Net change"]].T
