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

from init import display_as, isclose, USD, kUSD, FTE
from parameters import coal_import_price, external_cost, mining_parameter
from parameters import discount_rate

#%%


def benefits(system):
    """Tabulate the present value of various benefits from co-firing."""
    table = ['']
    table.append(system.cofiring_plant.name)
    table.append('-------------------')
    row2 = '{:30}' + '{:20.0f}'
    table.append(row2.format('Health', system.health_npv(discount_rate, external_cost)))
    table.append(row2.format('Emission reduction',
                             system.mitigation_npv(discount_rate, external_cost)))
    table.append(row2.format('Wages', system.wages_npv(discount_rate)))
    table.append(row2.format('Farmer earnings before tax',
                             system.farmer.net_present_value(discount_rate)))
    table.append(row2.format('Trader earnings before tax',
                             system.transporter.net_present_value(discount_rate)))
    return '\n'.join(table)


def coal_saved(system):
    """Tabulate the quantity and value of coal saved by cofiring."""
    col1 = system.coal_saved[1]
    col2 = display_as(col1 * coal_import_price, 'kUSD')

    row = '{:35}{:23.0f}'
    table = ['Coal saved at ' + str(system.cofiring_plant.name)]
    table.append(row.format('Amount of coal saved from co-firing', col1))
    table.append(row.format('Maximum benefit for trade balance', col2))
    return '\n'.join(table)

#%%


def as_table(emission_df):
    """Print a dataframe containing time series, showing only the second item of each element.

    Assumes that investment occured in period 0, so period 1 is the rate with cofiring.
    """
    return str(emission_df.applymap(lambda v: v[1]).T) + '\n'


def emissions(system):
    """Print the various emissions tables.

    There are many tables because:
        Emissions come from the plant, the supply, the straw supply, the open field burning
        Emissions can be  without cofiring / with cofiring / the difference
    """
    cofireplant = system.cofiring_plant
    plant = system.plant
    table = []
    table.append(plant.name + ' BASELINE EMISSION')
    table.append('Emission from power plant')
    table.append(as_table(plant.emissions()))
    table.append('Emission from coal supply')
    table.append(as_table(plant.coal_transporter().emissions()))
    table.append('Emission from open field burning')
    table.append(as_table(system.farmer.emissions_exante))
    table.append(plant.name + ' COFIRING EMISSION')
    table.append('Emission from power plant')
    table.append(as_table(cofireplant.emissions()))
    table.append('Emission from coal supply')
    table.append(as_table(cofireplant.coal_transporter().emissions()))
    table.append('Emission from straw supply')
    table.append(as_table(system.transporter.emissions()))
    table.append('Emission from open field burning')
    table.append(as_table(system.farmer.emissions()))
    table.append('-------')
    table.append(plant.name + ' EMISSION REDUCTION\n')
    table.append(as_table(system.emission_reduction(external_cost).T))
    return '\n'.join(table)

#%%


def year_1(df):
    """Replace the vector [a, b, b, b, .., b] by the quantity  b per year, in a dataframe.

    Object  y  denotes the unit symbol for "year".
    This assumes that investment occured in period 0, then steady state from period 1 onwards.
    """
    def projector(vector):
        scalar = vector[1]
        assert list(vector)[1:] == [scalar] * (len(vector) - 1)
        return scalar / y
    return df.applymap(projector).T


def emission_reductions(system_a, system_b):
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


def job_changes(system):
    """Tabulate the number of full time equivalent (FTE) jobs created/destroyed by cofiring."""
    cols = '{:25}{:12.1f}'
    cols2 = '{:25}{:12.1f}{:12.1f}'

    lines = ['Benefit from job creation: ' + system.plant.name + '\n']

    row7 = system.farmer.labor()[1]
    row1 = system.farmer.labor_cost()[1]
    row8 = system.transporter.driving_work()[1]
    row2 = system.transporter.driving_wages()[1]
    row11 = system.transporter.loading_work()[1]
    row12 = system.transporter.loading_wages()[1]
    row9 = system.cofiring_plant.biomass_om_work()[1]
    row3 = system.cofiring_plant.biomass_om_wages()[1]
    row10 = system.labor[1]
    row4 = system.wages[1]

    display_as(row7, 'FTE')
    display_as(row8, 'FTE')
    display_as(row9, 'FTE')
    display_as(row10, 'FTE')
    display_as(row11, 'FTE')

    lines.append(cols2.format('Biomass collection', row7, row1))
    lines.append(cols2.format('Biomass transportation', row8, row2))
    lines.append(cols2.format('Biomass loading', row11, row12))
    lines.append(cols2.format('O&M', row9, row3))
    lines.append(cols2.format('Total', row10, row4))
    lines.append('')
    lines.append(cols.format('Area collected', system.supply_chain.area()))
    lines.append(cols.format('Collection radius', system.supply_chain.collection_radius()))
    lines.append(cols.format('Maximum transport time', system.transporter.max_trip_time()))
    lines.append(cols.format('Number of truck trips', system.transporter.truck_trips[1]))
    lines.append('')
    lines.append('Mining job lost from co-firing at ' + system.plant.name + '\n')
    row = system.coal_work_lost(mining_parameter['productivity_underground'])[1]
    display_as(row, 'FTE')
    lines.append(cols.format('Job lost', row))
    lines.append(cols.format('Coal saved', system.coal_saved[1]))
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
