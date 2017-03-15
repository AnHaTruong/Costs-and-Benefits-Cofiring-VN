# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Regression testing : Emitter.py  vs.  emission.py
"""


from units import display_as
from emission_new import MD_plant_stack, MD_transport, MD_field, MDCofire_plant_stack
from emission_new import MDCofire_transport, MDCofire_field, MD_plant_ER, MD_transport_ER
from emission_new import MD_field_ER, MD_total_ER, MD_total_benefit

from emission_new import NB_plant_stack, NB_transport, NB_field, NBCofire_plant_stack
from emission_new import NBCofire_transport, NBCofire_field, NB_plant_ER, NB_transport_ER
from emission_new import NB_field_ER, NB_total_ER, NB_total_benefit

print("\nMong Duong 1 BASELINE\n")

print("Emissions from power plant\n", MD_plant_stack, "\n")

print("Emissions from transport\n", MD_transport, "\n")

print("Emission from open field burning\n", MD_field, "\n")

print("-------\nMong Duong 1 COFIRING\n")

print("Emissions from power plant\n", MDCofire_plant_stack, "\n")

print("Emissions from transport\n", MDCofire_transport, "\n")

print("Emission from open field burning\n", MDCofire_field, "\n")

print("-------\nMong Duong 1 REDUCTION\n")

print("From plant\n", MD_plant_ER, "\n")

print("From transport\n", MD_transport_ER, "\n")

print("From field\n", MD_field_ER, "\n")

print("Total emission reduction pollutants \n", MD_total_ER, "\n")

print("Benefit\n", display_as(MD_total_benefit, 'kUSD/y'))

print("==================\n")

print("\nNinh Binh BASELINE\n")

print("Emissions from power plant\n", NB_plant_stack, "\n")

print("Emissions from transport\n", NB_transport, "\n")

print("Emission from open field burning\n", NB_field, "\n")

print("-------\nNinh Binh COFIRING \n")

print("Emission from power plant\n", NBCofire_plant_stack, "\n")

print("Emissions from transportation\n", NBCofire_transport, "\n")

print("Emission from open field burning\n", NBCofire_field, "\n")

print("-------\nNinh Binh REDUCTION")

print("From plant\n", NB_plant_ER, "\n")

print("From transport\n", NB_transport_ER, "\n")

print("From field\n", NB_field_ER, "\n")

print("Total emission reduction pollutants \n", NB_total_ER, "\n")

print("Benefit\n", display_as(NB_total_benefit, 'kUSD/y'))
