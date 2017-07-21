# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Table of extra net income for the straw supply chains"""

from init import display_as

from parameters import MongDuong1System, NinhBinhSystem, collect_economics

display_as(collect_economics['winder_rental_cost'], 'USD/ha')


def print_farmer_income(system):
    """This table assumes that farmers are paid for transport.
    FIXME: truck rental and fuel costs
    FIXME: separate the bills for fieldside straw and transportation
    """
    area = system.supply_chain.farm_area()[1]
    revenue = system.farmer.income()[1] + system.supply_chain.transport_cost()[1]
    winder_cost = system.farmer.winder_rental_cost * area
    collect_cost = system.farmer.labor_cost()[1]
    loading_cost = system.transporter.loading_wages()[1]
    transport_cost = system.transporter.driving_wages()[1]

    total = revenue - winder_cost - collect_cost - loading_cost - transport_cost

    row = '{:20}' + '{:10.2f}' + '{:10.0f}'
    print(total)
    print('{:27}{:15}{:4}{:5.0f}'.format('', 'Per ha', 'For', area))
    print(row.format('Straw sales revenue', display_as(revenue / area, 'USD/ha'), revenue))
    print(row.format('- Winder rental', winder_cost / area, display_as(winder_cost, 'kUSD')))
    print(row.format('- Collection work', display_as(collect_cost / area, 'USD/ha'), collect_cost))
    print(row.format('- Loading work', display_as(loading_cost / area, 'USD/ha'), loading_cost))
    print(row.format('- Transport work', display_as(transport_cost / area, 'USD/ha'),
                     transport_cost))
    print(row.format('= Net income', display_as(total / area, 'USD/ha'), total))
    print()


print('Extra net income for supply chain around Mong Duong 1')
print_farmer_income(MongDuong1System)

print('Extra net income for supply chain around Ninh Binh')
print_farmer_income(NinhBinhSystem)
