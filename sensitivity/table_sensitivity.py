# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# table_sensitivityanalysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2020
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
"""Print the results of the sensitivity analysis."""

from sensitivity.one_at_a_time import table_sensitivity
from sensitivity.uncertainty import uncertainty_MD1, uncertainty_NB
from sensitivity.blackbox import f_MD1, f_NB


print(table_sensitivity(uncertainty_MD1, f_MD1, "Mong Duong 1"))
print(table_sensitivity(uncertainty_NB, f_NB, "Ninh Binh"))
