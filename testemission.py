# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Tests for the emission functions in  emission.py
"""

from parameters import MongDuong1, NinhBinh

from emission import emission_coal_combust, emission_coal_transport
from emission import emission_biomass_combust, emission_biomass_transport
from emission import total_emission_coal, total_emission_biomass
from emission import emission_reduction

print('')
head = '{:38}' + '{:18}' + '{:15}'
row = '{:35}' + '{:15.2f}'*2

print (head.format(' ', 'Mong Duong 1', 'Ninh Binh'))

print (row.format('emission from coal combustion',
                  emission_coal_combust(MongDuong1),
                  emission_coal_combust(NinhBinh)
                  )
      )

print (row.format('emission from coal transport',
                  emission_coal_transport(MongDuong1),
                  emission_coal_transport(NinhBinh)
                  )
      )      
 
print (row.format('emission from biomass combustion',
                  emission_biomass_combust(MongDuong1),
                  emission_biomass_combust(NinhBinh)
                  )
      )  
      
print (row.format('emission from biomass transport',
                  emission_biomass_transport(MongDuong1),
                  emission_biomass_transport(NinhBinh)
                  )
      )      

print (row.format('emission from coal',
                  total_emission_coal(MongDuong1),
                  total_emission_coal(NinhBinh)
                  )
      )

print (row.format('emission from biomass',
                  total_emission_biomass(MongDuong1),
                  total_emission_biomass(NinhBinh)
                  )
      )

print (row.format('emission reduction',
                  emission_reduction(MongDuong1),
                  emission_reduction(NinhBinh)
                  )
      )
