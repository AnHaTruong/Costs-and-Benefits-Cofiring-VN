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
"""Compare the levelized cost of electricity (LCOE) with and without cofiring."""
from natu.numpy import npv

from parameters import MongDuong1System, NinhBinhSystem
from parameters import discount_rate, tax_rate, depreciation_period


def lcoe(system):
    """Compare the LCOE with and without cofiring for one system."""
    def row_int(label, int_a, int_b):
        return '{:30}{:8.0f}{:20.0f}'.format(label, int_a, int_b)

    def row_float(label, float_x, float_y):
        return '{:30}{:8.1f}{:20.1f}'.format(label, float_x, float_y)

    def row_npv(label, vector_v, vector_w):
        return row_int(label, npv(discount_rate, vector_v), npv(discount_rate, vector_w))

    def row_npv_na(label, vector_w):
        return '{:43}{:20.0f}'.format(label, npv(discount_rate, vector_w))

    lines = [system.plant.name]

    lines.append('{:30}{:30}{:20}'.format('', "Reference", "Cofiring"))
    lines.append(row_int("Investment", system.plant.capital, system.cofiring_plant.capital))
    lines.append(row_npv("Fuel cost", system.plant.fuel_cost(), system.cofiring_plant.fuel_cost()))
    lines.append(row_npv("  Coal", system.plant.coal_cost, system.cofiring_plant.coal_cost))
    lines.append(row_npv_na("  Biomass", system.cofiring_plant.biomass_cost))
    lines.append(row_npv_na("    transportation", system.transport_cost))
    lines.append(row_npv_na("    straw at field", system.biomass_value))
    lines.append(row_npv(
        "O&M cost",
        system.plant.operation_maintenance_cost(),
        system.cofiring_plant.operation_maintenance_cost()))
    lines.append(row_npv(
        "  coal",
        system.plant.coal_om_cost(),
        system.cofiring_plant.coal_om_cost()))
    lines.append(row_npv_na(
        "  biomass",
        system.cofiring_plant.biomass_om_cost()))
    lines.append(row_npv(
        "Tax",
        system.plant.income_tax(tax_rate, depreciation_period),
        system.cofiring_plant.income_tax(tax_rate, depreciation_period)))
    lines.append(row_npv(
        "Sum of costs",
        system.plant.cash_out(tax_rate, depreciation_period),
        system.cofiring_plant.cash_out(tax_rate, depreciation_period)))
    lines.append(row_npv(
        "Electricity produced",
        system.plant.power_generation,
        system.cofiring_plant.power_generation))
    lines.append(row_float(
        "Levelized cost of electricity",
        system.plant.lcoe(discount_rate, tax_rate, depreciation_period),
        system.cofiring_plant.lcoe(discount_rate, tax_rate, depreciation_period)))

    return '\n'.join(lines)


print(lcoe(MongDuong1System))

print('')

print(lcoe(NinhBinhSystem))
