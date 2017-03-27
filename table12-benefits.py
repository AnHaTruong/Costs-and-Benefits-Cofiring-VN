# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print table for the present value of benefit from co-firing added up
    in benefitaddup.py
"""

from benefitaddup import benefit_add_up, total_benefit_addup, total_job_benefit
from farmerincome import total_income_benefit
from emission import emission_reduction_benefit, total_health_benefit
from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import discount_rate, time_horizon


print("Total benefit over", time_horizon, "years")
print("Discounted at", discount_rate)
print("")


def print_benefit_add_up(plant, cofiringplant):
    print('')
    print(cofiringplant.name)
    print('-------------------')
    row2 = '{:30}' + '{:20.0f}' + '{:20.0f}'
    print(row2.format('Health',
                      benefit_add_up(total_health_benefit, plant, cofiringplant),
                      float('NaN')
                      )
          )
    print(row2.format('Emission reduction',
                      benefit_add_up(emission_reduction_benefit, plant, cofiringplant),
                      float('NaN')
                      )
          )

    print(row2.format('Jobs',
                      benefit_add_up(total_job_benefit, plant, cofiringplant),
                      float('NaN')
                      )
          )

    print(row2.format('Farmer income',
                      benefit_add_up(total_income_benefit, plant, cofiringplant),
                      benefit_add_up(total_income_benefit, plant, cofiringplant)
                      )
          )
    print(row2.format('Total',
                      total_benefit_addup(plant, cofiringplant),
                      float('NaN')
                      )
          )

print_benefit_add_up(MongDuong1, MongDuong1Cofire)

print_benefit_add_up(NinhBinh, NinhBinhCofire)
