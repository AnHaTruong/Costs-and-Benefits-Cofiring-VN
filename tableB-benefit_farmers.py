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

from parameters import MongDuong1Cofire, NinhBinhCofire

from farmerincome import farmer_income, bm_sell_revenue, total_income_benefit

print('')

row = '{:20}' + '{:23.6G}'


def print_income(cofireplant):
    col1 = bm_sell_revenue(cofireplant)
    col2 = farmer_income(cofireplant)
    col3 = total_income_benefit(cofireplant)

    print(row.format('biomass sell revenue', col1))

    print(row.format('farmer income per ha', col2))

    print(row.format('total benefit', col3))

print('total benefit from farmers extra income Mong Duong 1')
print('')
print_income(MongDuong1Cofire)

print('')
print('total benefit from farmers extra income Ninh Binh')
print('')
print_income(NinhBinhCofire)
