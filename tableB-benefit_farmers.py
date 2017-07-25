# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Table of extra net income for the straw supply chains"""

from init import display_as

from parameters import MongDuong1System, NinhBinhSystem


def print_farmer_income(system):
    """This table prints farmers and transport revenue / expenses.
    """
    print("Balance sheets of biomass supply sector players")
    print(system.plant.name)

    area = system.farmer.farm_area[1]
    revenue = system.farmer.revenue[1]
    winder_cost = system.farmer.capital_cost[1]
    fuel_cost = system.farmer.fuel_cost()[1]
    collect_cost = system.farmer.labor_cost()[1]
    total = revenue - winder_cost - collect_cost - fuel_cost

    print('                                      over', area)
    print('                            Total         Per ha')
    row = '{:20}' + '{:10.0f}' + '{:10.2f}'
    print(row.format('Straw revenue', revenue, display_as(revenue / area, 'USD/ha')))
    print(row.format('- Winder rental',
                     display_as(winder_cost, 'kUSD'),
                     display_as(winder_cost / area, 'USD/ha')))
    print(row.format('- Winder fuel', fuel_cost, display_as(fuel_cost / area, 'USD/ha')))
    print(row.format('- Collection work', collect_cost, display_as(collect_cost / area, 'USD/ha')))
    print(row.format('= Net income', total, display_as(total / area, 'USD/ha')))

    print()
    revenue = system.transporter.revenue[1]
    loading_cost = system.transporter.loading_wages()[1]
    driving_cost = system.transporter.driving_wages()[1]
    fuel_cost = system.transporter.fuel_cost()[1]
    capital_cost = system.transporter.capital_cost()[1]
    total = revenue - loading_cost - driving_cost
    row = '{:20}' + '{:10.0f}'
    print(row.format('Transport revenue', revenue))
    print(row.format('- Handling work', loading_cost))
    print(row.format('- Driving work', driving_cost))
    print(row.format('- Truck fuel', fuel_cost))
    print(row.format('- Truck rental', capital_cost))
    print(row.format('= Net income', total))
    print()


print_farmer_income(MongDuong1System)
print_farmer_income(NinhBinhSystem)
