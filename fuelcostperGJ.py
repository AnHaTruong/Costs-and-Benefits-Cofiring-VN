# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Calculation of fuel cost per GJ"""
from parameters import  biomass_heat_value, MongDuong1, NinhBinh
from biomasscost import bm_unit_cost
from units import print_with_unit

def coal_cost_perGJ(plant):
    return plant.coal_price / plant.coal_supply.heat_value


def bm_cost_perGJ(plant):
    return bm_unit_cost(plant) / biomass_heat_value
    

#print(print_with_unit(coal_cost_perGJ(MongDuong1), 'USD/GJ'))
#print(print_with_unit(coal_cost_perGJ(NinhBinh), 'USD/GJ'))
#print(print_with_unit(bm_cost_perGJ(MongDuong1), 'USD/GJ'))
#print(print_with_unit(bm_cost_perGJ(NinhBinh), 'USD/GJ'))