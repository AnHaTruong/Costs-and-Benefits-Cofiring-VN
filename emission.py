# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#  Greenhouse gas emissions reduction assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Greenhouse gas and pollutant emissions assessment of a co-firing project.
   Total emission include emission from fuel combustion, fuel transportation and open field burning
   Climate benefit and health benefit from GHG and air pollutant emission reduction
"""
from parameters import specific_cost


def emission_reduction_benefit(plant, cofireplant):
    return cofireplant.emission_reduction(specific_cost)['CO2']['Benefit'][1]


def total_health_benefit(plant, cofireplant):
    return cofireplant.emission_reduction(specific_cost).ix['Benefit'].drop('CO2').sum()[1]
