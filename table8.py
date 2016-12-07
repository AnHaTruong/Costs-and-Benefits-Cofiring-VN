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
row = '{:10}' + '{:18.2f}' * 3 + '{:15.0f}'


print('')


def print_health(plant):

    print(head.format('Pollutant',
                      'Base emission',
                      'Co-firing emission',
                      'Emission reduction ',
                      'Health benefit'
                     )
         )
    col1 = health_benefit_so2(plant)
    col2 = health_benefit_pm10(plant)
    col3 = health_benefit_nox(plant)
    col4 = total_health_benefit(plant)
    col5 = so2_emission_cofiring(plant)
    col6 = pm10_emission_cofiring(plant)
    col7 = nox_emission_cofiring(plant)
    col8 = so2_emission_base(plant)
    col9 = pm10_emission_base (plant)
    col10 = nox_emission_base(plant)

    col1.display_unit = 'USD/y'
    col2.display_unit = 'USD/y'
    col3.display_unit = 'USD/y'
    col4.display_unit = 'kUSD/y'
    col5.display_unit = 't/y'
    col6.display_unit = 't/y'
    col7.display_unit = 't/y'
    col8.display_unit = 't/y'
    col9.display_unit = 't/y'
    col10.display_unit = 't/y'

    print(row.format('SO2',
                     col8,
                     col5,
                     so2_emission_reduction(plant),
                     col1
                    )
         )

    print(row.format('PM10',
                     col9,
                     col6,
                     pm10_emission_reduction(plant),
                     col2
                    )
         )

    print(row.format('NOx',
                     col10,
                     col7,
                     nox_emission_reduction(plant),
                     col3
                    )
         )

    print('Total health benefit ', col4)

print('Health benefit - Mong Duong 1')
print_health(MongDuong1)

print('')

print('Health benefit - Ninh Binh')
print_health(NinhBinh)
