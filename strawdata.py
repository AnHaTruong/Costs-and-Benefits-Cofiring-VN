# Economic of co-firing in two power plants in Vietnam
#
# Rice data processing
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#


import pandas as pd
from units import km, ha, t, y
from parameters import residue_to_product_ratio_straw, straw_collection_fraction
from parameters import straw_selling_proportion
from natu.numpy import mean


"""Read rice production data from excel file"""
data = pd.read_excel('Data/Rice_production_2014_GSO.xlsx',)
df = pd.DataFrame(data)
df = df.set_index('Province')

# Calculate straw yield of each province from rice yield and Residue-to-Product Ratio (RPR) of straw
residue_to_product_ratio = pd.DataFrame({'Residue to product ratio straw':[residue_to_product_ratio_straw]})
df['straw yield'] = df['Rice yield (ton/ha)'] *t/ha/y * residue_to_product_ratio['Residue to product ratio straw'].values

#Calculate biomass available density from rice cultivation area density,collection fraction and selling fraction of straw
collection_fraction = pd.DataFrame({'straw collection fraction':[straw_collection_fraction]})
selling_proportion = pd.DataFrame({'straw selling proportion':[straw_selling_proportion]})

# Rice planted density is the ratio between cultivation area and total area
df['rice planted density'] = df['Cultivation area (ha)']*ha/(df['Total area (ha)']*ha)

# Calculate straw density of each provinces
df['straw density'] = (df['straw yield'] *
                       df['rice planted density'] *
                       collection_fraction['straw collection fraction'].values *
                       selling_proportion['straw selling proportion'].values
                      )

MongDuong1_straw_density1 = df.loc['Quang Ninh', 'straw density'] # straw density of Quang Ninh province
MongDuong1_straw_density2 = mean([df.loc['Bac Giang', 'straw density'], # straw density of adjacent provinces
                                  df.loc['Hai Duong', 'straw density'],
                                  df.loc['Hai Phong', 'straw density']
                                 ])
NinhBinh_straw_density = df.loc['Ninh Binh', 'straw density']
