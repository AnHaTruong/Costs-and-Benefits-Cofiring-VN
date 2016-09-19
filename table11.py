# Economic of co-firing in two power plants in Vietnam
#
#  
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
# 
""" Print table for the effect of co-firing on coal saving and national trade 
    balance in coalsaved.py
"""

from coalsaved import coal_saved, coal_import_saving
from parameters import MongDuong1, NinhBinh

print('')

row = '{:35}' + '{:23.0f}'

def print_coal_saved(plant):
    col1 = coal_saved(plant)
    col2 = coal_import_saving(plant)
    
    col1.display_unit = 't/y'
    col2.display_unit = 'kUSD/y'
    
    print (row.format('Amount of coal saved from co-firing', col1))
    print (row.format('Maximum benefit for trade balance', col2))
    

print('Coal saved benefit Mong Duong1')
print('')
print_coal_saved(MongDuong1)

print('')
print('Coal saved benefit Ninh Binh')
print('')
print_coal_saved(NinhBinh)
