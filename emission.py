
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

from init import display_as

from parameters import MongDuong1, NinhBinh, MongDuong1Cofire, NinhBinhCofire
from parameters import emission_factor, specific_cost
from Emitter import Emitter
from strawburned import straw_burned_infield


# Mong Duong 1

MD_field = Emitter({'Straw': straw_burned_infield(MongDuong1)},
                   emission_factor)

MDCofire_field = Emitter({'Straw': straw_burned_infield(MongDuong1) - MongDuong1Cofire.biomass_used
                          },
                         emission_factor)

# Calculate emission reduction
MD_plant_ER = (MongDuong1.stack.emissions()["Total"]
               - MongDuong1Cofire.stack.emissions()["Total"])

MD_transport_ER = (MongDuong1.coal_transporter().emissions()["Total"]
                   - MongDuong1Cofire.coal_transporter().emissions()["Total"])

MD_field_ER = MD_field.emissions()["Total"] - MDCofire_field.emissions()["Total"]

MD_total_ER = MD_plant_ER + MD_transport_ER + MD_field_ER

# Calculate benefit from emission reduction
MD_total_benefit = MD_total_ER * specific_cost
display_as(MD_total_benefit, 'kUSD')

# Create pandas DataFrame from emission reduction Series
list_of_series = [MD_plant_ER, MD_transport_ER, MD_field_ER, MD_total_ER, MD_total_benefit]
row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
MD_ER_table = pd.DataFrame(list_of_series, index=row)

# Split benefit from GHG emission reduction and health benefit
MD_ER_benefit = MD_total_benefit['CO2']
MD_health_benefit = MD_total_benefit.drop('CO2').sum()


# Ninh Binh

NB_field = Emitter({'Straw': straw_burned_infield(NinhBinh)}, emission_factor)

NBCofire_field = Emitter({'Straw': straw_burned_infield(NinhBinh) - NinhBinhCofire.biomass_used},
                         emission_factor)

# Calculate emission reduction
NB_plant_ER = (NinhBinh.stack.emissions()["Total"]
               - NinhBinhCofire.stack.emissions()["Total"])

NB_transport_ER = (NinhBinh.coal_transporter().emissions()["Total"]
                   - NinhBinhCofire.coal_transporter().emissions()["Total"])

NB_field_ER = NB_field.emissions()["Total"] - NBCofire_field.emissions()["Total"]
NB_total_ER = NB_plant_ER + NB_transport_ER + NB_field_ER

# Calculate benefit from emission reduction
NB_total_benefit = NB_total_ER * specific_cost
display_as(NB_total_benefit, 'kUSD')

# Create pandas DataFrame from emission reduction Series
list_of_series = [NB_plant_ER, NB_transport_ER, NB_field_ER, NB_total_ER, NB_total_benefit]
row = ['Plant', 'Transport', 'Field', 'Total', 'Benefit']
NB_ER_table = pd.DataFrame(list_of_series, index=row)

# Split benefit from GHG emission reduction and health benefit
NB_ER_benefit = NB_total_benefit['CO2']
NB_health_benefit = NB_total_benefit.drop('CO2').sum()


#

def emission_reduction_benefit(plant, cofiringplant):
    """ return the monetary benefit from greenhouse gas emission reduction"""
    plant_emissions = (
        plant.stack.emissions()["Total"]["CO2"]
        + plant.coal_transporter().emissions()["Total"]["CO2"])

    cofiringplant_emissions = (
        cofiringplant.stack.emissions()["Total"]["CO2"]
        + cofiringplant.coal_transporter().emissions()["Total"]["CO2"]
        + cofiringplant.straw_supply.transport_emissions()["Road transport"]["CO2"])

    return (plant_emissions - cofiringplant_emissions) * specific_cost['CO2']
