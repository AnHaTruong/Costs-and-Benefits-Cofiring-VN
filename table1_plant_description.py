# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Print table 1 for Technical parameters of the plants."""

from natu.units import y

from parameters import MongDuong1System, NinhBinhSystem

MongDuong1 = MongDuong1System.plant
NinhBinh = NinhBinhSystem.plant

print('\nTable 1. Technical parameters\n')

print('{:24}{:>20}{:>20}'.format('Parameter', 'Mong Duong 1', 'Ninh Binh'))

print('{:24}{:>20}{:>20}'.format('Comissioning year',
                                 MongDuong1.parameter.commissioning,
                                 NinhBinh.parameter.commissioning)
      )
print('{:24}{:>20}{:>20}'.format('Boiler technology',
                                 MongDuong1.parameter.boiler_technology,
                                 NinhBinh.parameter.boiler_technology)
      )
print('{:24}{:>20.0f}{:>17.0f}'.format('Installed capacity',
                                       MongDuong1.parameter.capacity / y,
                                       NinhBinh.parameter.capacity / y)
      )
print('{:24}{:>20.2f}{:>20.2f}'.format('Capacity factor',
                                       MongDuong1.parameter.capacity_factor,
                                       NinhBinh.parameter.capacity_factor)
      )
print('{:24}{:>20.0f}{:>16.0f}'.format('Coal consumption',
                                       MongDuong1.coal_used[0],
                                       NinhBinh.coal_used[0])
      )
print('{:24}{:>20.0f}{:>14.0f}'.format('Heat value of coal',
                                       MongDuong1.parameter.coal.heat_value,
                                       NinhBinh.parameter.coal.heat_value)
      )
print('{:24}{:>20.4f}{:>20.4f}'.format('Plant efficiency',
                                       MongDuong1.plant_efficiency[0],
                                       NinhBinh.plant_efficiency[0])
      )
print('{:24}{:>20.4f}{:>20.4f}'.format('Boiler efficiency',
                                       MongDuong1.parameter.boiler_efficiency[0],
                                       NinhBinh.parameter.boiler_efficiency[0])
      )
