# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# table_sensitivityanalysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Print the results of the sensitivity analysis."""

from pandas import DataFrame

from sensitivity.one_at_a_time import sensitivity_runs

print("Results of the sensitivity analysis.")
print()
print("Result: business value.")
print(DataFrame(sensitivity_runs["business_value"]))
print()
print("Result: external value.")
print(DataFrame(sensitivity_runs["external_value"]))
