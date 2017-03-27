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
""" Print the result of farmer extra income assessment from farmerincome.py"""

from init import display_as

from parameters import MongDuong1Cofire, NinhBinhCofire
from parameters import winder_rental_cost, straw

display_as(winder_rental_cost, 'USD/ha')

def print_income(supply_chain):
    row1 = supply_chain.farm_revenue_per_ha(straw.price)
    row3 = supply_chain.farm_income_per_ha(winder_rental_cost, straw.price)
    row4 = supply_chain.farm_area()[1]
    row5 = supply_chain.farm_income(winder_rental_cost, straw.price)[1]

    row = '{:25}' + '{:23.6G}'
    print()
    print(row.format('Revenue from straw sales', row1))
    print(row.format('- Winder rental', winder_rental_cost))
    print(row.format('= Net income', row3))
    print(row.format('* Surface', row4))
    print(row.format('= Total social benefit', row5))
    print()

print('Extra net income for farmers around Mong Duong 1')
print_income(MongDuong1Cofire.straw_supply)

print('Extra net income for farmers around Ninh Binh')
print_income(NinhBinhCofire.straw_supply)
