# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

from init import display_as

from parameters import MongDuong1Cofire, NinhBinhCofire
from parameters import winder_rental_cost, straw

display_as(winder_rental_cost, 'USD/ha')


def print_income(supply_chain):
    total = supply_chain.farm_income(winder_rental_cost, straw.price)[1]
    area = supply_chain.farm_area()[1]
    row1col1 = supply_chain.farm_revenue_per_ha(straw.price)
    row1col2 = display_as(row1col1 * area, 'kUSD')
    row2col1 = winder_rental_cost
    row2col2 = display_as(row2col1 * area, 'kUSD')
    row3col1 = supply_chain.farm_income_per_ha(winder_rental_cost, straw.price)
    row3col2 = display_as(row3col1 * area, 'kUSD')

    row = '{:20}' + '{:10.0f}' + '{:10.0f}'
    print(total)
    print('{:27}{:15}{:4}{:5.0f}'.format('', 'Per ha', 'For', area))
    print(row.format('Straw sales revenue', row1col1, row1col2))
    print(row.format('- Winder rental', row2col1, row2col2))
    print(row.format('= Net income', row3col1, row3col2))
    print()

print('Extra net income for farmers around Mong Duong 1')
print_income(MongDuong1Cofire.straw_supply)

print('Extra net income for farmers around Ninh Binh')
print_income(NinhBinhCofire.straw_supply)
