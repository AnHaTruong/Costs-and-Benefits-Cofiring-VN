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

from pandas import set_option

from manuscript1.parameters import MongDuong1System, NinhBinhSystem
from model.tables import balance_jobs


set_option('display.float_format', '{:,.1f}'.format)

print("""Jobs creation and destruction in the co-firing scenario.

                             Mong Duong 1  Ninh Binh""")

print(balance_jobs(MongDuong1System, NinhBinhSystem))
