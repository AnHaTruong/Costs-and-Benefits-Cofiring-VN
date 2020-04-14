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

from sensitivity.one_at_a_time import sensitivity_runs_MD1, sensitivity_runs_NB

print("Results of the sensitivity analysis for Mong Duong 1 case.")
print()
print("Result: business value.")
print(DataFrame(sensitivity_runs_MD1["business_value"]))
print()
print("Result: external value.")
print(DataFrame(sensitivity_runs_MD1["external_value"]))
print()
print("Results of the sensitivity analysis for Ninh Binh case.")
print()
print("Result: business value.")
print(DataFrame(sensitivity_runs_NB["business_value"]))
print()
print("Result: external value.")
print(DataFrame(sensitivity_runs_NB["external_value"]))
