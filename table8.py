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
head = '{:22}' * 2 + '{:27}' * 3
row = '{:10}' + '{:15.2f}' * 4

print('Health benefit - Mong Duong 1')
print('')
print (head.format('Pollutant',
                   'Base emission',
                   'Co-firing emission',
                   'Emission reduction ',
                   'Health benefit'
                   )
       )

print (row.format('SO2',
                  so2_emission_base(MongDuong1),
                  so2_emission_cofiring(MongDuong1),
                  so2_emission_reduction(MongDuong1),
                  health_benefit_so2(MongDuong1)
                  )
       )

print (row.format('PM10',
                  pm10_emission_base(MongDuong1),
                  pm10_emission_cofiring(MongDuong1),
                  pm10_emission_reduction(MongDuong1),
                  health_benefit_pm10(MongDuong1)
                  )
       )

print (row.format('NOx',
                  nox_emission_base(MongDuong1),
                  nox_emission_cofiring(MongDuong1),
                  nox_emission_reduction(MongDuong1),
                  health_benefit_nox(MongDuong1)
                  )
       )

print ('Total',total_health_benefit(MongDuong1))
print('')

print('Health benefit - Ninh Binh')
print('')
print (head.format('Pollutant',
                   'Base emission',
                   'Co-firing emission',
                   'Emission reduction ',
                   'Health banefit'
                   )
       )

print (row.format('SO2',
                  so2_emission_base(NinhBinh),
                  so2_emission_cofiring(NinhBinh),
                  so2_emission_reduction(NinhBinh),
                  health_benefit_so2(NinhBinh)
                  )
       )

print (row.format('PM10',
                  pm10_emission_base(NinhBinh),
                  pm10_emission_cofiring(NinhBinh),
                  pm10_emission_reduction(NinhBinh),
                  health_benefit_pm10(NinhBinh)
                  )
       )

print (row.format('NOx',
                  nox_emission_base(NinhBinh),
                  nox_emission_cofiring(NinhBinh),
                  nox_emission_reduction(NinhBinh),
                  health_benefit_nox(NinhBinh)
                  )
       )
print ('Total',total_health_benefit(NinhBinh))
