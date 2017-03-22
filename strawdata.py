
# Economic of co-firing in two power plants in Vietnam
#
# Rice data processing
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#


import pandas as pd
from natu.units import ha, t
# from parameters import residue_to_product_ratio_straw, straw_collection_fraction
# from parameters import straw_selling_proportion
from natu.numpy import mean
from natu.math import fsum

straw_collection_fraction = 0.5  # Refer to (Leinonen and Nguyen 2013)
straw_selling_proportion = 0.79  # Refer to (Leinonen and Nguyen 2013)
residue_to_product_ratio_straw = 1.0

"""Read rice production data from excel file"""
data = pd.read_excel('Data/Rice_production_2014_GSO.xlsx',)
df = pd.DataFrame(data)
df = df.set_index('Province')

# Calculate straw yield of each province from rice yield and straw Residue-to-Product Ratio (RPR)
residue_to_product_ratio = pd.DataFrame({'Residue to product ratio straw':
                                         [residue_to_product_ratio_straw]})

# Yield per period, that is per year
df['straw yield'] = (df['Rice yield (ton/ha)'] * t / ha *
                     residue_to_product_ratio['Residue to product ratio straw'].values)

# Calculate biomass available density from rice cultivation area density,
# collection fraction and selling fraction of straw
collection_fraction = pd.DataFrame({'straw collection fraction': [straw_collection_fraction]})
selling_proportion = pd.DataFrame({'straw selling proportion': [straw_selling_proportion]})

# Rice planted density is the ratio between cultivation area and total area
df['rice planted density'] = df['Cultivation area (ha)'] * ha / (df['Total area (ha)'] * ha)

# Calculate straw density of each provinces
df['straw density'] = (df['straw yield'] *
                       df['rice planted density'] *
                       collection_fraction['straw collection fraction'].values *
                       selling_proportion['straw selling proportion'].values
                       )

df['straw production'] = df['rice production (ton)'] * t * residue_to_product_ratio_straw

MongDuong1_straw_density1 = df.loc['Quang Ninh', 'straw density'] # straw density of Quang Ninh province

MongDuong1_straw_density2 = mean([df.loc['Bac Giang', 'straw density'], # straw density of adjacent provinces
                                  df.loc['Hai Duong', 'straw density'],
                                  df.loc['Hai Phong', 'straw density']
                                  ])
NinhBinh_straw_density = df.loc['Ninh Binh', 'straw density']

MongDuong1_straw_production = fsum([df.loc['Bac Giang', 'straw production'],
                                    df.loc['Hai Duong', 'straw production'],
                                    df.loc['Hai Phong', 'straw production'],
                                    df.loc['Quang Ninh', 'straw production']
                                    ])
MongDuong1_average_straw_yield = mean([df.loc['Bac Giang', 'straw yield'],
                                       df.loc['Hai Duong', 'straw yield'],
                                       df.loc['Hai Phong', 'straw yield'],
                                       df.loc['Quang Ninh', 'straw yield']
                                       ])
NinhBinh_straw_production = df.loc['Ninh Binh', 'straw production']
NinhBinh_average_straw_yield = df.loc['Ninh Binh', 'straw yield']

#print("# This file automatically generated, DO NOT EDIT\n")
#print("MongDuong1_straw_density1 =", str(MongDuong1_straw_density1))

