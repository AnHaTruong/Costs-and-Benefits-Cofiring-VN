# Economic of co-firing in two power plants in Vietnam
#
# Biomass cost
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Calculate the unit price of biomass for co-firing as delivered to the plant
    Unit price include fix price and transportation cost
"""

import math
from units import km
from natu.math import sqrt
from natu.numpy import mean
from parameters import MongDuong1, NinhBinh
from units import print_with_unit
from strawdata import df

from biomassrequired import biomass_required
from parameters import transport_tariff, tortuosity_factor
from parameters import biomass_fix_cost, biomass_ratio, zero_km

#
# import math, sympy
#   simplify(integrate(integrate(x, (x, r, R)),(t, 0, pi)) )
#
# The transport activity (t km) is the order one moment
#   tortuosity * simplify(integrate(integrate(x * x, (x, r, R)),(t, 0, pi)) )
#   tortuosity * (R**3 - r**3) / 3

#"""Read rice production data from excel file"""
#data = pd.read_excel('Data/Rice_production_2014_GSO.xlsx',)
#df = pd.DataFrame(data)
#df = df.set_index('Province')
#
## Calculate straw yield of each province from rice yield and Residue-to-Product Ratio (RPR) of straw
#residue_to_product_ratio = pd.DataFrame({'Residue to product ratio straw':[residue_to_product_ratio_straw]})
#df['straw yield'] = df['Rice yield (ton/ha)'] *t/ha/y * residue_to_product_ratio['Residue to product ratio straw'].values
#
##Calculate biomass available density from rice cultivation area density,collection fraction and selling fraction of straw
#collection_fraction = pd.DataFrame({'straw collection fraction':[straw_collection_fraction]})
#selling_proportion = pd.DataFrame({'straw selling proportion':[straw_selling_proportion]})
#
## Rice planted density is the ratio between cultivation area and total area
#df['rice planted density'] = df['Cultivation area (ha)']*ha/(df['Total area (ha)']*ha)
#
## Calculate straw density of each provinces
#df['straw density'] = (df['straw yield'] *
#                       df['rice planted density'] *
#                       collection_fraction['straw collection fraction'].values *
#                       selling_proportion['straw selling proportion'].values
#                      )


def collection_area(plant):
    """
    Biomass is collected from two semi annulus centered on the plant.    
    The surface of a semi annulus is  pi * (R**2 - r**2) / 2
        
    Ninh Binh case: collection area is a disk
    both semi annulus have zero smaller radius, identical larger radius, 
    and the same biomass density
    
    Mong Duong 1 case: collection area is a half disk
    1st semi annulus has zero smaller radius, larger radius = distance from plant to Quang Ninh province border
    2nd semi annulus has smaller radius = larger radius of 1st semi annulus
    1st and 2nd semi annulus have different straw density
    straw density of 1st semi annulus is the straw density of Quang Ninh provice
    straw density of 2nd semi annulus is the average of straw density in adjacent provinces
        
    >>> from parameters import *
    >>> print_with_unit(collection_area(MongDuong1), 'km2')
    3393.1 km2
    >>> print_with_unit(collection_area(NinhBinh), 'km2')
    581.28 km2
    """
    if plant == MongDuong1:
        small_radius_semi_annulus1 = 0 * km
        large_radius_semi_annulus1 = 50 * km # which is the distance from the plant to Quang Ninh border
        area_semi_annulus1 = math.pi * (large_radius_semi_annulus1**2 - small_radius_semi_annulus1**2)/2
        straw_supplied_semi_annulus1 = area_semi_annulus1 * df.loc['Quang Ninh', 'straw density']
        straw_supplied_semi_annulus2 = biomass_required(MongDuong1) - straw_supplied_semi_annulus1
        straw_density_adjacent_provinces = mean([df.loc['Bac Giang', 'straw density'],
                                                 df.loc['Hai Duong', 'straw density'],
                                                 df.loc['Hai Phong', 'straw density']
                                                ])
        area_semi_annulus2 = straw_supplied_semi_annulus2 / straw_density_adjacent_provinces
        
        return area_semi_annulus1 + area_semi_annulus2
        
    if plant == NinhBinh:
        return biomass_required(NinhBinh) / df.loc['Ninh Binh', 'straw density']


def radius_of_disk(area):
    return sqrt(area / math.pi)

def collection_radius(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(collection_radius(MongDuong1), 'km')
    68.265 km
    >>> print_with_unit(collection_radius(NinhBinh), 'km')
    13.6025 km
    """
    if plant == MongDuong1:
        small_radius_semi_annulus1 = 0 * km
        large_radius_semi_annulus1 = 50 * km
        small_radius_semi_annulus2 =  large_radius_semi_annulus1
        area_semi_annulus1 = math.pi * (large_radius_semi_annulus1**2 - small_radius_semi_annulus1**2)/2
              
        if biomass_ratio == 0:
            return zero_km
        else:
#        we need to calculate the large radius of 2nd semi annulus.
            return sqrt((collection_area(MongDuong1) - area_semi_annulus1)/math.pi*2 + small_radius_semi_annulus2**2)

    if plant == NinhBinh:
        return radius_of_disk(collection_area(NinhBinh))


# Use an intermediate function "transportation activity" in t km (reused to compute emissions)
# Dig the 5 whys - the units should have prevented error on degree
def bm_transportation_cost(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(bm_transportation_cost(MongDuong1), 'USD/t')
    6.13067 USD/t
    >>> print_with_unit(bm_transportation_cost(NinhBinh), 'USD/t')
    1.2216 USD/t
    """
    # FIXME: No magic numbers
    # FIXME: Check the integral : pi and cube missing ? Add reference
    # FIXME: Non uniform density
    return 2.0 / 3.0 * collection_radius(plant) * tortuosity_factor * transport_tariff


def bm_unit_cost(plant):
    """
    >>> from parameters import *
    >>> print_with_unit(bm_unit_cost(MongDuong1), 'USD/t')
    43.3907 USD/t
    >>> print_with_unit(bm_unit_cost(NinhBinh), 'USD/t')
    38.4816 USD/t
    """
    return bm_transportation_cost(plant) + biomass_fix_cost

if __name__ == "__main__":
    import doctest
    doctest.testmod()
