# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Print the tables for manuscript 'Costs and benefits of co-firing'.

Costs and benefits of co-firing rice straw in two Vietnamese coal power plants
An Ha Truong, Minh Ha-Duong
2017-2019
"""

from pandas import DataFrame, set_option
from model.utils import kg, t, g, km

from manuscript1.parameters import emission_factor

set_option("display.max_colwidth", 40)
set_option("display.max_columns", 10)
set_option("display.width", 80)

data = DataFrame.from_dict(emission_factor).transpose()

set_option("display.float_format", "{:9,.1f} kg/t".format)
print(data.loc[["6b_coal", "4b_coal", "straw_boiler", "straw_open"]] / (kg / t))

set_option("display.float_format", "{:8,.5F} g/tkm".format)
print(data.loc[["conveyor_belt", "road_transport", "barge_transport"]] / (g / t / km))
