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

from parameters import MongDuong1System, NinhBinhSystem
from parameters import discount_rate, tax_rate, depreciation_period, feedin_tariff


def tableC(system, tariff):
    def printRowInt(label, a, b):
        print('{:30}{:8.0f}{:20.0f}'.format(label, a, b))

    def printRowFloat(label, x, y):
        print('{:30}{:8.4f}{:20.4f}'.format(label, x, y))

    def printRowNPV(label, v, w):
        printRowInt(label, npv(discount_rate, v), npv(discount_rate, w))

    def printRowNPV_na(label, w):
        print('{:43}{:20.0f}'.format(label, npv(discount_rate, w)))

    print(system.plant.name)
    print('{:30}{:30}{:20}'.format('', "Reference", "Cofiring"))
    printRowInt("Investment", system.plant.capital, system.cofiring_plant.capital)
    printRowNPV("Fuel cost", system.plant.fuel_cost(), system.cofiring_plant.fuel_cost())
    printRowNPV("  Coal", system.plant.coal_cost(), system.cofiring_plant.coal_cost())
    printRowNPV_na("  Biomass", system.cofiring_plant.biomass_cost)
    printRowNPV_na("    transportation", system.transport_cost)
    printRowNPV_na("    straw at field", system.biomass_value)
    printRowNPV("O&M cost",
                system.plant.operation_maintenance_cost(),
                system.cofiring_plant.operation_maintenance_cost())
    printRowNPV("  coal", system.plant.coal_om_cost(), system.cofiring_plant.coal_om_cost())
    printRowNPV_na("  biomass", system.cofiring_plant.biomass_om_cost())
    printRowNPV("Tax",
                system.plant.income_tax(tariff, tax_rate, depreciation_period),
                system.cofiring_plant.income_tax(tariff, tax_rate, depreciation_period))
    printRowNPV("Sum of costs",
                system.plant.cash_out(tariff, tax_rate, depreciation_period),
                system.cofiring_plant.cash_out(tariff, tax_rate, depreciation_period))
    printRowNPV("Electricity produced",
                system.plant.power_generation,
                system.cofiring_plant.power_generation)
    printRowFloat("Levelized cost of electricity",
                  system.plant.lcoe(tariff, discount_rate, tax_rate, depreciation_period),
                  system.cofiring_plant.lcoe(tariff, discount_rate, tax_rate, depreciation_period))


tableC(MongDuong1System, feedin_tariff['MD'])

print('')

tableC(NinhBinhSystem, feedin_tariff['NB'])
