# Economic of co-firing in two power plants in Vietnam
#
# Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#

MWtokW = 1000   # conversion factor
GWtokW = 1000000   # conversion factor


class PowerPlant:
    pass

MongDuong1 = PowerPlant()

MongDuong1.commissioning = 2015   # year
MongDuong1.boiler_technology = "CFB"
MongDuong1.capacity = 1080*MWtokW   # kW
MongDuong1.generation = 6500*GWtokW   # kWh/yr
MongDuong1.coal_heat_value = 19.4   # Mj/kg
MongDuong1.base_coal_consumption = 2.75  # Mt/yr
MongDuong1.base_plant_efficiency = 38.84  # percent
MongDuong1.base_boiler_efficiency = 87.03  # percent

NinhBinh = PowerPlant()

NinhBinh.commissioning = 1974  # year
NinhBinh.boiler_technology = "PC"
NinhBinh.capacity = 100*MWtokW  # kW
NinhBinh.generation = 750*GWtokW  # kWh/yr
NinhBinh.coal_heat_value = 25.3  # Mj/kg
NinhBinh.base_coal_consumption = 0.42  # Mt/yr
NinhBinh.base_plant_efficiency = 21.77  # percent
NinhBinh.base_boiler_efficiency = 81.61  # percent

MongDuong1.capital_cost = 50  # USD/kW
MongDuong1.coal_price = 52.69  # USD/ton
MongDuong1.fix_om_cost = 32.34  # USD/kW.year
MongDuong1.variable_om_cost = 0.6  # UScent/kWh
# Computed separately. Assumes 5% co-firing
MongDuong1.biomass_required = 259107.274137779  # ton/year
MongDuong1.biomass_unit_cost = 41.3111153541657  # USD/ton

NinhBinh.capital_cost = 100  # USD/kW
NinhBinh.coal_price = 83.83  # USD/ton
NinhBinh.fix_om_cost = 32.34  # USD/kW.year
NinhBinh.variable_om_cost = 0.6  # UScent/kWh
# Computed separately. Assumes 5% co-firing
NinhBinh.biomass_required = 53362.0062849769  # ton/year
NinhBinh.biomass_unit_cost = 38.154337591058  # USD/ton

biomass_ratio = 0.05  # Percent of energy that comes from biomass
    # energy meaning both heat and electricity produced
time_horizon = 20  # years
discount_rate = 8.78/100  # per year
tax_rate = 0.25  # Corporate tax in Vietnam
exchange_rate = 21473  # VND/USD
electricity_tariff_VND = 1158.1  # VND/kWh
electricity_tariff_USD = electricity_tariff_VND / exchange_rate
