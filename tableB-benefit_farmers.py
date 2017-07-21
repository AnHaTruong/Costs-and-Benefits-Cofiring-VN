# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Table of extra net income for the straw supply chains"""

from init import display_as

from parameters import MongDuong1Cofire, NinhBinhCofire
from parameters import straw, collect_economics, truck_economics

display_as(collect_economics['winder_rental_cost'], 'USD/ha')


def print_income(supply_chain):
    area = supply_chain.farm_area()[1]
    revenue = supply_chain.cost(straw.price)[1]
    winder_cost = collect_economics['winder_rental_cost'] * area
    collect_cost = supply_chain.farm_wages(collect_economics)[1]
    loading_cost = supply_chain.loading_wages(truck_economics)[1]
    transport_cost = supply_chain.transport_wages(truck_economics)[1]

    total = supply_chain.farm_profit(straw.price, collect_economics, truck_economics)[1]

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
print_income(MongDuong1Cofire.straw_supply)

print('Extra net income for supply chain around Ninh Binh')
print_income(NinhBinhCofire.straw_supply)
