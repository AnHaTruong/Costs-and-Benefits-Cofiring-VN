# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# Instantiate technology data in Vietnam Technology Catalogue (Jakob Lundsager et al. 2019)
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Reproduce LCOE as calculated by DEA in EOR19 using parameter from VN Technology Catalogue."""

from model.utils import USD, kWh

discount_rate = 0.1
electricity_price = 0.08 * USD / kWh
tax_rate = 0.0
depreciation_period = 10
economic_horizon = 20
