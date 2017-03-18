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
import pandas as pd
from natu.units import t, km, y

from init import v_zeros, display_as, time_step

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import emission_factor, NB_Coal, specific_cost
from Emitter import Emitter
from strawburned import straw_burned_infield


zero_transport = v_zeros * t * km / y


# Define objects
MD_transport = Emitter({'Road transport': zero_transport,
                        'Barge transport': zero_transport},
                       emission_factor,
                       {'CO2': 0.0}
                       )

MD_field = Emitter({'Straw': straw_burned_infield(MongDuong1)},
                   emission_factor)

MDCofire_transport = Emitter({'Road transport': MongDuong1Cofire.active_chain.transport_tkm() / y,
                              'Barge transport': zero_transport
                              },
                             emission_factor,
                             {'CO2': 0.0}
                             )

MDCofire_coal_transport = Emitter({'Barge transport': zero_transport}, emission_factor)

MDCofire_straw_emissions = MongDuong1Cofire.active_chain.transport_emissions()

MDCofire_field = Emitter({'Straw': straw_burned_infield(MongDuong1) - MongDuong1Cofire.biomass_used
                          },
                         emission_factor)

# Calculate emission reduction
MD_plant_ER = (MongDuong1.plant_stack.emissions()["Total"]
               - MongDuong1Cofire.plant_stack.emissions()["Total"])

MD_transport_CO2 = (MD_transport.emissions()["Total"]
                    - MDCofire_coal_transport.emissions()["Total"]["CO2"]
                    - MDCofire_straw_emissions["Total"]["CO2"])

MD_transport_pollutant = pd.Series([0.0 * t / y, 0.0 * t / y, 0.0 * t / y],
                                   index=['SO2', 'PM10', 'NOx'])

MD_transport_ER = MD_transport_CO2.append(MD_transport_pollutant)

MD_field_ER = MD_field.emissions()["Total"] - MDCofire_field.emissions()["Total"]

MD_total_ER = MD_plant_ER + MD_transport_ER + MD_field_ER

# Calculate benefit from emission reduction
MD_total_benefit = MD_total_ER * specific_cost
display_as(MD_total_benefit, 'kUSD/y')

# Create pandas DataFrame from emission reduction Series
list_of_series = [MD_plant_ER, MD_transport_ER, MD_field_ER, MD_total_ER, MD_total_benefit]
row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
MD_ER_table = pd.DataFrame(list_of_series, index=row)

# Split benefit from GHG emission reduction and health benefit
MD_ER_benefit = MD_total_benefit['CO2']
MD_health_benefit = MD_total_benefit.drop('CO2').sum()


# Ninh Binh
# Define objects

NB_transport_activity = {'Road transport': zero_transport,
                         'Barge transport': NinhBinh.coal_used * NB_Coal.transport_distance * 2
                         }

NB_transport_activity = {'Road transport': zero_transport,
                         'Barge transport': NinhBinh.coal_used * NB_Coal.transport_distance * 2
                         }

NB_transport = Emitter(NB_transport_activity, emission_factor, {'CO2': 0.0})

NB_field = Emitter({'Straw': straw_burned_infield(NinhBinh)}, emission_factor)

NBCofire_transport = Emitter({'Road transport': NinhBinhCofire.active_chain.transport_tkm() / y,
                              'Barge transport': (NinhBinhCofire.coal_used
                                                  * NB_Coal.transport_distance * 2)
                              },
                             emission_factor,
                             {'CO2': 0.0})

NBCofire_field = Emitter({'Straw': straw_burned_infield(NinhBinh) - NinhBinhCofire.biomass_used},
                         emission_factor)

# Calculate emission reduction
NB_plant_ER = (NinhBinh.plant_stack.emissions()["Total"]
               - NinhBinhCofire.plant_stack.emissions()["Total"])

NB_transport_CO2 = NB_transport.emissions()["Total"] - NBCofire_transport.emissions()["Total"]
NB_transport_pollutant = pd.Series([0.0 * t / y, 0.0 * t / y, 0.0 * t / y],
                                   index=['SO2', 'PM10', 'NOx'])
NB_transport_ER = NB_transport_CO2.append(NB_transport_pollutant)

NB_field_ER = NB_field.emissions()["Total"] - NBCofire_field.emissions()["Total"]
NB_total_ER = NB_plant_ER + NB_transport_ER + NB_field_ER

# Calculate benefit from emission reduction
NB_total_benefit = NB_total_ER * specific_cost
display_as(NB_total_benefit, 'kUSD/y')

# Create pandas DataFrame from emission reduction Series
list_of_series = [NB_plant_ER, NB_transport_ER, NB_field_ER, NB_total_ER, NB_total_benefit]
row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
NB_ER_table = pd.DataFrame(list_of_series, index=row)

# Split benefit from GHG emission reduction and health benefit
NB_ER_benefit = NB_total_benefit['CO2']
NB_health_benefit = NB_total_benefit.drop('CO2').sum()


# OLD FILE CONTENT

def emission_coal_combust_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal combustion
       when there is no co-firing

    """
    return emission_factor[plant.coal.name]["CO2"] * plant.coal_used[1]


def emission_coal_transport_base(plant):
    """return the greenhouse gas emission in tonCO2eq from coal transportation
       in no co-firing case. transported distance is 2 times of coal transport
       distance because round trip is accounted

    """
    return plant.coal.ef_transport * 2 * plant.coal.transport_distance * plant.coal_used[1]


def emission_coal_combust_cofire(cofiringplant):
    """ emission from coal combustion when co-fire
    """
    return emission_factor[cofiringplant.coal.name]["CO2"] * cofiringplant.coal_used[1]


def emission_coal_transport_cofire(cofiringplant):
    """emission from coal transportation when co-fire

    """
    return (cofiringplant.coal.ef_transport
            * 2 * cofiringplant.coal.transport_distance
            * cofiringplant.coal_used[1]
            )


def emission_biomass_combust(cofiringplant):
    """return the emission from biomass combustion with co-firing

    """
    return emission_factor[cofiringplant.biomass.name]["CO2"] * cofiringplant.biomass_used[1]


def emission_biomass_transport(cofiringplant):
    mass = (cofiringplant.biomass.ef_transport
            * cofiringplant.active_chain.transport_tkm()[1] / time_step
            )
    mass.display_unit = 't/y'
    return mass


def total_emission_coal(plant):
    """emission from coal in base case. only account for the percentage of coal
       substituted by biomass8
    """
    return emission_coal_combust_base(plant) + emission_coal_transport_base(plant)


def total_emission_cofire(cofiringplant):
    """sum of emission from biomass combustion and biomass transportation for
       co-firing case
    """
    return (emission_biomass_combust(cofiringplant)
            + emission_biomass_transport(cofiringplant)
            + emission_coal_combust_cofire(cofiringplant)
            + emission_coal_transport_cofire(cofiringplant)
            )


def emission_reduction(plant, cofiringplant):
    """different between total emission from coal (base case) and total
       emission from biomass (co-firing case)
    """
    return total_emission_coal(plant) - total_emission_cofire(cofiringplant)


def emission_reduction_benefit(plant, cofiringplant):
    """ return the monetary benefit from greenhouse gas emission reduction"""
    return emission_reduction(plant, cofiringplant) * specific_cost['CO2']
