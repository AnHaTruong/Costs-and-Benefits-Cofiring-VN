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

from natu.numpy import npv
from natu.units import y, ha, t

from init import display_as, isclose, USD, kUSD, FTE
from parameters import coal_import_price, external_cost, mining_parameter
from parameters import discount_rate, tax_rate, depreciation_period

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


def lcoe(system):
    """Compare the LCOE with and without cofiring for one system."""
    def row_int(label, int_a, int_b):
        return '{:30}{:8.0f}{:20.0f}'.format(label, int_a, int_b)

    def row_float(label, float_x, float_y):
        return '{:30}{:8.1f}{:20.1f}'.format(label, float_x, float_y)

    def row_npv(label, vector_v, vector_w):
        return row_int(label, npv(discount_rate, vector_v), npv(discount_rate, vector_w))

    def row_npv_na(label, vector_w):
        return '{:43}{:20.0f}'.format(label, npv(discount_rate, vector_w))

    lines = [system.plant.name]

    lines.append('{:30}{:30}{:20}'.format('', "Reference", "Cofiring"))
    lines.append(row_int("Investment", system.plant.capital, system.cofiring_plant.capital))
    lines.append(row_npv("Fuel cost", system.plant.fuel_cost(), system.cofiring_plant.fuel_cost()))
    lines.append(row_npv("  Coal", system.plant.coal_cost, system.cofiring_plant.coal_cost))
    lines.append(row_npv_na("  Biomass", system.cofiring_plant.biomass_cost))
    lines.append(row_npv_na("    transportation", system.transport_cost))
    lines.append(row_npv_na("    straw at field", system.biomass_value))
    lines.append(row_npv(
        "O&M cost",
        system.plant.operation_maintenance_cost(),
        system.cofiring_plant.operation_maintenance_cost()))
    lines.append(row_npv(
        "  coal",
        system.plant.coal_om_cost(),
        system.cofiring_plant.coal_om_cost()))
    lines.append(row_npv_na(
        "  biomass",
        system.cofiring_plant.biomass_om_cost()))
    lines.append(row_npv(
        "Tax",
        system.plant.income_tax(tax_rate, depreciation_period),
        system.cofiring_plant.income_tax(tax_rate, depreciation_period)))
    lines.append(row_npv(
        "Sum of costs",
        system.plant.cash_out(tax_rate, depreciation_period),
        system.cofiring_plant.cash_out(tax_rate, depreciation_period)))
    lines.append(row_npv(
        "Electricity produced",
        system.plant.power_generation,
        system.cofiring_plant.power_generation))
    lines.append(row_float(
        "Levelized cost of electricity",
        system.plant.lcoe(discount_rate, tax_rate, depreciation_period),
        system.cofiring_plant.lcoe(discount_rate, tax_rate, depreciation_period)))

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


def technical_parameters(system_a, system_b):
    """Tabulate the technical parameters for two plants."""
    plant_a = system_a.plant
    plant_b = system_b.plant
    table = []

    table.append('{:24}{:>20}{:>20}'.format('Parameter', plant_a.name, plant_b.name))

    table.append('{:24}{:>20}{:>20}'.format('Comissioning year',
                                            plant_a.parameter.commissioning,
                                            plant_b.parameter.commissioning))

    table.append('{:24}{:>20}{:>20}'.format('Boiler technology',
                                            plant_a.parameter.boiler_technology,
                                            plant_b.parameter.boiler_technology))

    table.append('{:24}{:>20.0f}{:>17.0f}'.format('Installed capacity',
                                                  plant_a.parameter.capacity / y,
                                                  plant_b.parameter.capacity / y))

    table.append('{:24}{:>20.2f}{:>20.2f}'.format('Capacity factor',
                                                  plant_a.parameter.capacity_factor,
                                                  plant_b.parameter.capacity_factor))

    table.append('{:24}{:>20.0f}{:>16.0f}'.format('Coal consumption',
                                                  plant_a.coal_used[0],
                                                  plant_b.coal_used[0]))

    table.append('{:24}{:>20.0f}{:>14.0f}'.format('Heat value of coal',
                                                  plant_a.parameter.coal.heat_value,
                                                  plant_b.parameter.coal.heat_value))

    table.append('{:24}{:>20.4f}{:>20.4f}'.format('Plant efficiency',
                                                  plant_a.           plant_efficiency[0],
                                                  plant_b.           plant_efficiency[0]))

    table.append('{:24}{:>20.4f}{:>20.4f}'.format('Boiler efficiency',
                                                  plant_a.parameter.boiler_efficiency[0],
                                                  plant_b.parameter.boiler_efficiency[0]))

    return '\n'.join(table)

#%% TODO: Delete because redundant with the next two


def upstream_benefits(system):
    """Tabulate farmers and transport revenue / expenses tables for one system."""
    lines = ["Balance sheets of biomass supply sector players"]
    lines.append(system.plant.name)

    area = system.farmer.farm_area[1]
    lines.append('                                      over ' + str(area))

    lines.append('                            Total         Per ha')

    row = '{:20}' + '{:10.0f}' + '{:10.2f}'

    revenue = system.farmer.revenue[1]
    lines.append(row.format(
        'Straw revenue',
        revenue,
        display_as(revenue / area, 'USD/ha')))

    winder_cost = system.farmer.capital_cost()[1]
    lines.append(row.format(
        '- Winder rental',
        display_as(winder_cost, 'kUSD'),
        display_as(winder_cost / area, 'USD/ha')))

    fuel_cost = system.farmer.fuel_cost()[1]
    lines.append(row.format(
        '- Winder fuel',
        fuel_cost,
        display_as(fuel_cost / area, 'USD/ha')))

    collect_cost = system.farmer.labor_cost()[1]
    lines.append(row.format(
        '- Collection work',
        collect_cost,
        display_as(collect_cost / area, 'USD/ha')))

    total = revenue - winder_cost - collect_cost - fuel_cost
    lines.append(row.format(
        '= Net income',
        total,
        display_as(total / area, 'USD/ha')))

    lines.append('')

    revenue = system.transporter.revenue[1]
    loading_cost = system.transporter.loading_wages()[1]
    driving_cost = system.transporter.driving_wages()[1]
    fuel_cost = system.transporter.fuel_cost()[1]
    capital_cost = system.transporter.capital_cost()[1]
    total = revenue - loading_cost - driving_cost
    row = '{:20}' + '{:10.0f}'
    lines.append(row.format('Transport revenue', revenue))
    lines.append(row.format('- Handling work', loading_cost))
    lines.append(row.format('- Driving work', driving_cost))
    lines.append(row.format('- Truck fuel', fuel_cost))
    lines.append(row.format('- Truck rental', capital_cost))
    lines.append(row.format('= Net income', total))
    lines.append('')
    return '\n'.join(lines)

#%%


def balance_sheet_farmer(system_a, system_b):
    """Summarize the economic implications for the farmers."""
    headings = ['Straw revenue',
                '- Winder rental',
                '- Winder fuel',
                '- Collection work']

    def cash_flows(farmer):
        return pd.Series(
            data=[farmer.revenue[1],
                  - farmer.capital_cost()[1],
                  - farmer.fuel_cost()[1],
                  - farmer.labor_cost()[1]],
            index=headings)

    farm_a = system_a.farmer
    farm_b = system_b.farmer
    perha_a = cash_flows(farm_a) / farm_a.farm_area[1] / (USD / ha)
    perha_b = cash_flows(farm_b) / farm_b.farm_area[1] / (USD / ha)
    contents = [
        cash_flows(farm_a) / (1000 * USD), perha_a,
        cash_flows(farm_b) / (1000 * USD), perha_b]
    headers = ["Total", "Per ha",
               "Total", "Per ha"]
    df = pd.DataFrame(
        data=contents,
        index=headers)
    df["= Net income"] = df.sum(axis=1)
    df["Unit"] = ['kUSD', 'USD/ha', 'kUSD', 'USD/ha']
    return df[["Unit"] + headings + ["= Net income"]].T

#%%


def balance_sheet_transporter(system_a, system_b):
    """Summarize the economic implications for the transporters."""
    headings = ['Transport revenue',
                '- Truck rental',
                '- Truck fuel',
                '- Handling work',
                '- Driving work']

    def cash_flows(transporter):
        return pd.Series(
            data=[transporter.revenue[1],
                  - transporter.capital_cost()[1],
                  - transporter.fuel_cost()[1],
                  - transporter.loading_wages()[1],
                  - transporter.driving_wages()[1]],
            index=headings)

    transport_a = system_a.transporter
    transport_b = system_b.transporter
    pertrip_a = cash_flows(transport_a) / transport_a.truck_trips[1]
    pertrip_b = cash_flows(transport_b) / transport_b.truck_trips[1]
    contents = [
        cash_flows(transport_a) / (1000 * USD), pertrip_a / USD,
        cash_flows(transport_b) / (1000 * USD), pertrip_b / USD]
    headers = ["Total", "Per_trip",
               "Total", "Per_trip"]
    df = pd.DataFrame(
        data=contents,
        index=headers)
    df["= Net income"] = df.sum(axis=1)
    df["Unit"] = ['kUSD', 'USD', 'kUSD', 'USD']
    return df[["Unit"] + headings + ["= Net income"]].T

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
