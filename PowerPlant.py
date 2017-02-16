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
                 boiler_technology, coal_heat_value, plant_efficiency,
                 boiler_efficiency):
        self.capacity = capacity
        self.capacity_factor = capacity_factor
        self.commissioning = commissioning
        self.boiler_technology = boiler_technology
        self.power_generation = capacity * capacity_factor * time_step
        self.elec_sale = self.power_generation  # Capacity factor was net of self consumption
        self.coal_heat_value = coal_heat_value
        self.plant_efficiency = plant_efficiency
        self.base_boiler_efficiency = boiler_efficiency
        self.base_coal_consumption = capacity * capacity_factor / plant_efficiency / coal_heat_value
