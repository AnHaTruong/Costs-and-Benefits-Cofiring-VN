# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Tabulate of extra net income for the farmer and the transporter."""

from init import display_as

from parameters import MongDuong1System, NinhBinhSystem


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


print(upstream_benefits(MongDuong1System))
print(upstream_benefits(NinhBinhSystem))
