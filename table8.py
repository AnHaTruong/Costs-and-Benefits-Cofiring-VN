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

from parameters import MongDuong1, NinhBinh

from health import so2_emission_base, pm10_emission_base, nox_emission_base
from health import so2_emission_cofiring, pm10_emission_cofiring, nox_emission_cofiring
from health import so2_emission_reduction, pm10_emission_reduction, nox_emission_reduction
from health import health_benefit_so2, health_benefit_pm10, health_benefit_nox
from health import total_health_benefit

print('')
head = '{:22}' * 2 + '{:22}' * 3
row = '{:10}' + '{:15.2f}' * 4


print('')


def print_health(plant):
    
    print (head.format('Pollutant',
                       'Base emission',
                       'Co-firing emission',
                       'Emission reduction ',
                       'Health benefit'
                       )
           )    

    print (row.format('SO2',
                      so2_emission_base(plant),
                      so2_emission_cofiring(plant),
                      so2_emission_reduction(plant),
                      health_benefit_so2(plant)
                      )
           )

    print (row.format('PM10',
                      pm10_emission_base(plant),
                      pm10_emission_cofiring(plant),
                      pm10_emission_reduction(plant),
                      health_benefit_pm10(plant)
                      )
           )

    print (row.format('NOx',
                      nox_emission_base(plant),
                      nox_emission_cofiring(plant),
                      nox_emission_reduction(plant),
                      health_benefit_nox(plant)
                      )
           )
    
    print ('Total health benefit ',total_health_benefit(plant))

print('Health benefit - Mong Duong 1')
print_health(MongDuong1)

print('')

print('Health benefit - Ninh Binh')
print_health(NinhBinh)
