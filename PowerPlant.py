# Economic of co-firing in two power plants in Vietnam
#
# Physical units
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_step

class PowerPlant:

    def __init__(self, capacity, capacity_factor, commissioning,
                 boiler_technology, coal_heat_value, base_plant_efficiency):
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.power_generation = capacity * capacity_factor * time_step
        self.elec_sale = self.power_generation
        self.coal_heat_value = coal_heat_value
        self.base_plant_efficiency = base_plant_efficiency
        self.base_coal_consumption = capacity * capacity_factor / base_plant_efficiency / coal_heat_value
