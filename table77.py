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

from emission import emission_coal_combust_base, emission_coal_transport_base
from emission import emission_biomass_combust, emission_biomass_transport
from emission import total_emission_coal, total_emission_biomass
from emission import emission_reduction

print('')
row = '{:35}' + '{:16.2f}'



def print_emission(plant):
    """Print table 7-Emission reduction from co-firing """
    
    col1 = emission_biomass_combust(plant)
    col2 = emission_biomass_transport(plant)
    col3 = total_emission_biomass(plant)
    
    col1.display_unit = 't/y'
    col2.display_unit = 't/y'
    col3.display_unit = 't/y'
    
    print(row.format('emission from coal combustion',
                     emission_coal_combust_base(plant),
                    )
         )

    print(row.format('emission from coal transport',
                     emission_coal_transport_base(plant),
                    )
         )

    print(row.format('emission from biomass combustion',
                     col1,
                    )
         )

    print(row.format('emission from biomass transport',
                     col2,
                    )
         )

    print(row.format('emission from coal',
                     total_emission_coal(plant),
                    )
         )

    print(row.format('emission from biomass',
                     col3,
                    )
         )

    print(row.format('emission reduction',
                     emission_reduction(plant),
                    )
         )

print('Greenhouse gas emission reduction Mong Duong 1')
print_emission(MongDuong1)
print('')

print('Greenhouse gas emission reduction NinhBinh')
print_emission(NinhBinh)

