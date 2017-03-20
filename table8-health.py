# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Print out the result on health benefits of co-firing project from health.py
"""

from init import display_as
from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire

from health import *
from strawburned import so2_emission_field_base, pm10_emission_field_base, nox_emission_field_base

print('')
head = '{:22}' * 2 + '{:22}' * 7
row = '{:10}' + '{:18.2f}' * 7 + '{:15.0f}'


print('')


def print_health(plant, cofiringplant):

    print(head.format('Pollutant',
                      'Field emission base',
                      'Plant emission base',
                      'Base emission',
                      'Field emission cofire',
                      'Plant emission co-fire',
                      'Co-firing emission',
                      'Emission reduction ',
                      'Health benefit'
                     )
         )
    col11 = so2_emission_field_base(plant)
    col12 = pm10_emission_field_base(plant)
    col13 = nox_emission_field_base(plant)
    col21 = so2_emission_plant_base(plant)
    col22 = pm10_emission_plant_base(plant)
    col23 = nox_emission_plant_base(plant)
    col31 = so2_emission_base(plant)
    col32 = pm10_emission_base(plant)
    col33 = nox_emission_base(plant)
    col41 = so2_emission_field_cofire(plant, cofiringplant)
    col42 = pm10_emission_field_cofire(plant, cofiringplant)
    col43 = nox_emission_field_cofire(plant, cofiringplant)
    col51 = so2_emission_plant_cofire(plant, cofiringplant)
    col52 = pm10_emission_plant_cofire(plant, cofiringplant)
    col53 = nox_emission_plant_cofire (plant, cofiringplant)
    col61 = so2_emission_cofire(plant, cofiringplant)
    col62 = pm10_emission_cofire(plant, cofiringplant)
    col63 = nox_emission_cofire(plant, cofiringplant)
    col71 = so2_emission_reduction(plant, cofiringplant)
    col72 = pm10_emission_reduction(plant, cofiringplant)
    col73 = nox_emission_reduction(plant, cofiringplant)
    col81 = health_benefit_so2(plant, cofiringplant)
    col82 = health_benefit_pm10(plant, cofiringplant)
    col83 = health_benefit_nox(plant, cofiringplant)
    col9 = total_health_benefit(plant, cofiringplant)

    display_as(col81, 'kUSD')
    display_as(col82, 'kUSD')
    display_as(col83, 'kUSD')
    display_as(col9, 'kUSD')

    print(row.format('SO2', col11, col21, col31, col41, col51, col61, col71, col81))

    print(row.format('PM10', col12, col22, col32, col42, col52, col62, col72, col82))

    print(row.format('NOx', col13, col23, col33, col43, col53, col63, col73, col83))

    print('Total health benefit ', col9)

print('Health benefit - Mong Duong 1')
print_health(MongDuong1, MongDuong1Cofire)

print('')

print('Health benefit - Ninh Binh')
print_health(NinhBinh, NinhBinhCofire)
