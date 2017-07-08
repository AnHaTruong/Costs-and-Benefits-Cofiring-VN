# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity (LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016-2017
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""Compares the LCOE with and without cofiring"""
from natu.numpy import npv

from parameters import MongDuong1, MongDuong1Cofire, NinhBinh, NinhBinhCofire
from parameters import discount_rate, tax_rate, depreciation_period, feedin_tariff
from PowerPlant import CofiringPlant


def tableC(plant, tariff):
    def printRowInt(label, quantity):
        print('{:30}{:8.0f}'.format(label, quantity))

    def printRowFloat(label, value):
        print('{:30}{:8.4f}'.format(label, value))

    def printRowNPV(label, vector):
        printRowInt(label, npv(discount_rate, vector))

    print("Levelized cost of electricity - " + plant.name + "\n")
    printRowInt("Investment", plant.capital)
    printRowNPV("Fuel cost", plant.fuel_cost())
    if isinstance(plant, CofiringPlant):
        printRowNPV("  Coal", plant.coal_cost())
        printRowNPV("  Biomass", plant.straw_supply.cost(plant.biomass.price))
        printRowNPV("    transportation", plant.straw_supply.transport_cost())
        printRowNPV("    straw at field", plant.straw_supply.field_cost(plant.biomass.price))
    printRowNPV("O&M cost", plant.operation_maintenance_cost())
    if isinstance(plant, CofiringPlant):
        printRowNPV("  coal", plant.coal_om_cost())
        printRowNPV("  biomass", plant.biomass_om_cost())
    printRowNPV("Tax", plant.income_tax(tariff,
                                        tax_rate,
                                        depreciation_period))
    printRowNPV("Sum of costs", plant.cash_out(tariff,
                                               tax_rate,
                                               depreciation_period))
    printRowNPV("Electricity produced", plant.power_generation)
    printRowFloat("LCOE", plant.lcoe(tariff,
                                     discount_rate,
                                     tax_rate,
                                     depreciation_period))


tableC(MongDuong1, feedin_tariff['MD'])
print('')
tableC(MongDuong1Cofire, feedin_tariff['MD'])

print('')

tableC(NinhBinh, feedin_tariff['NB'])
print('')
tableC(NinhBinhCofire, feedin_tariff['NB'])
