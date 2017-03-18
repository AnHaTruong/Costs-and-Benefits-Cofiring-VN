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
from benefitaddup import benefit_add_up_new
from health import total_health_benefit
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit
from job import total_job_benefit
from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from emission import MD_ER_benefit, NB_ER_benefit, MD_health_benefit, NB_health_benefit

row = '{:35}' + '{:23.0f}'


def print_benefit_add_up(plant, cofiringplant):
    print(row.format('Added up health benefit',
                     new_benefit_add_up(total_health_benefit, plant, cofiringplant)
                     )
          )
    print(row.format('Added up emission reduction benefit',
                     new_benefit_add_up(emission_reduction_benefit, plant, cofiringplant)
                     )
          )
    print(row.format('Added up job benefit',
                     new_benefit_add_up(total_job_benefit, plant, cofiringplant)
                     )
          )
    print(row.format('Added up farmer income benefit',
                     benefit_add_up(total_income_benefit, plant)
                     )
          )
    print(row.format('Added up total benefit',
                     total_benefit_addup(plant, cofiringplant)
                     )
          )

print('\nOld version\n')
print('Added up benefit Mong Duong1\n')
print_benefit_add_up(MongDuong1, MongDuong1Cofire)

print('\nAdded up benefit Ninh Binh\n')
print_benefit_add_up(NinhBinh, NinhBinhCofire)

print('==================')
print('New version')
print('Added up benefit Mong Duong1\n')
print('Added up health benefit', benefit_add_up_new(MD_health_benefit))
print('Added up emission reduction benefit', benefit_add_up_new(MD_ER_benefit))
print('\nAdded up benefit Ninh Binh\n')
print('Added up health benefit', benefit_add_up_new(NB_health_benefit))
print('Added up emission reduction benefit', benefit_add_up_new(NB_ER_benefit))
