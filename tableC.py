# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity(LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""test for the LCOE funcction in file lcoe.py"""

from parameters import MongDuong1, NinhBinh

from LCOE import cap_rec_factor, lcoe
from LCOE import lcoe_cap_return, lcoe_fix_om, lcoe_bm_cost, lcoe_variable_om


print('')
print('capacity recovery factor', (cap_rec_factor()))

print('')
head = '{:22}' + '{:30}'*2
row = '{:22}' + '{:4.4f}'

#print (head.format(' ', 'Mong Duong 1', 'Ninh Binh'))


def print_lcoe(plant):
    
    col1 = lcoe_cap_return(plant)
    col2 = lcoe_fix_om(plant)
    col3 = lcoe_bm_cost(plant)
    col4 = lcoe_variable_om(plant)
    col5 = lcoe(plant)
    
    col1.display_unit = 'USD/(kW*hr)'
    col2.display_unit = 'USD/(kW*hr)'
    col3.display_unit = 'USD/(kW*hr)'
    col4.display_unit = 'USD/(kW*hr)'
    col5.display_unit = 'USD/(kW*hr)'
       
    print(row.format('lcoe cap return', col1))
    print(row.format('lcoe fix O&M', col2))
    print(row.format('lcoe biomass cost', col3))
    print(row.format('lcoe variable cost', col4))
    print(row.format('lcoe', col5))
    
    
print('Levelized cost of electricity Mong Duong 1')
print('')
print_lcoe(MongDuong1)

print('')
print('')
print('Levelized cost of electricity Ninh Binh')
print('')

print_lcoe(NinhBinh)
