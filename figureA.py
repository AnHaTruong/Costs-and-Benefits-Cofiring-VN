# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:18:19 2016

@author: anha
draw map of coal power plants in Vietnam
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


"""Draw map of Vietnam"""
fig = plt.figure(figsize=(12, 16))
ax = fig.add_subplot(111)

map = Basemap(projection='merc', lat_0=24, lon_0=110,
              resolution='h', area_thresh=0.1,
              llcrnrlon=101.0, llcrnrlat=6.0,
              urcrnrlon=118.0, urcrnrlat=24.0)

map.fillcontinents(color='lightgrey')
map.drawmapboundary()

"""Color Vietnam differently"""
map.readshapefile(r'Data/VNM_adm_shp/VNM_adm1', 'VNM_adm1', drawbounds=False)

patches = []

for info, shape in zip(map.VNM_adm1_info, map.VNM_adm1):
    x, y = zip(*shape)
    patches.append(Polygon(np.array(shape), True))

ax.add_collection(PatchCollection(patches,
                                  facecolor='#ade2d2',
                                  edgecolor='#62a390',
                                  linewidths=1.,
                                  zorder=2))

"""Add Paracel and Spratly Islands"""
lons = [112.0, 115.0]
lats = [16.5, 9.0]
x, y = map(lons, lats)
map.plot(x, y, linestyle='None', marker='o', markerfacecolor='#62a390', markersize=8)

labels = ['Paracel Islands', 'Spratly Island']
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt, ypt, label)

"""Read data from excel file"""
data = pd.read_excel('Data/List_of_coal_power_plants.xlsx', skiprows=[1])

"""Create empty lists for latitudes, longitudes, number of unit and capacity"""
lats, lons = [], []
unit = []
size = []
""" Store latitudes, longitudes, number of unit and capacity in lists"""
for index, row in data.iterrows():
    lats.append(row[2])
    lons.append(row[3])
    unit.append(row[5])
    size.append(row[6])

"""Plot the plant based on lats and lons, and capacity"""
for lon, lat, size in zip(lons, lats, size):
    x, y = map(lons, lats)
    msize = ((size / math.pi)**0.5) / 2
#    print(msize)
    map.plot(x, y, 'ro', markersize=msize)

# """Display number of unit for each plant"""
# for unit, lons, lats in zip(unit, lons, lats):
#    plt.text(lats, lons, unit)

plt.savefig('figureA.pdf', format='pdf')
