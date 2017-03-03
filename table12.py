# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print table for the present value of benefit from co-firing added up
    in benefitaddup.py
"""

from benefitaddup import benefit_add_up, new_benefit_add_up, total_benefit_addup
from health import total_health_benefit
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit
from job import total_job_benefit
from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire

print('')

row = '{:35}' + '{:23.0f}'


def print_benefit_add_up(plant, cofiringplant):
    col1 = benefit_add_up(total_health_benefit, plant)
    col2 = new_benefit_add_up(emission_reduction_benefit, plant, cofiringplant)
    col3 = new_benefit_add_up(total_job_benefit, plant, cofiringplant)
    col4 = benefit_add_up(total_income_benefit, plant)
    col5 = total_benefit_addup(plant, cofiringplant)

    col1.display_unit = 'kUSD'
    col2.display_unit = 'kUSD'
    col3.display_unit = 'kUSD'
    col4.display_unit = 'kUSD'
    col5.display_unit = 'kUSD'


    print (row.format('Added up health benefit', col1))
    print (row.format('Added up emission reduction benefit', col2))
    print (row.format('Added up job benefit', col3))
    print (row.format('Added up farmer income benefit', col4))
    print (row.format('Added up total benefit', col5))


print('Added up benefit Mong Duong1')
print('')
print_benefit_add_up(MongDuong1, MongDuong1Cofire)

print('')
print('Added up benefit Ninh Binh')
print('')
print_benefit_add_up(NinhBinh, NinhBinhCofire)


