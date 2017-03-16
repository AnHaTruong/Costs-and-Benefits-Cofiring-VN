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

from emission_new import MD_plant_stack, MD_transport, MD_field, MDCofire_plant_stack
from emission_new import MDCofire_transport, MDCofire_field, MD_ER_table

from emission_new import NB_plant_stack, NB_transport, NB_field, NBCofire_plant_stack
from emission_new import NBCofire_transport, NBCofire_field, NB_ER_table

print("\nMong Duong 1 BASELINE EMISSIONS\n")

print("Emissions from power plant\n", MD_plant_stack.emissions().T, "\n")

print("Emissions from transport\n", MD_transport.emissions().T, "\n")

print("Emission from open field burning\n", MD_field.emissions().T, "\n")

print("-------\nMong Duong 1 COFIRING EMISSIONS\n")

print("Emissions from power plant\n", MDCofire_plant_stack.emissions().T, "\n")

print("Emissions from transport\n", MDCofire_transport.emissions().T, "\n")

print("Emission from open field burning\n", MDCofire_field.emissions().T, "\n")

print("-------\nMong Duong 1 EMISSION REDUCTION\n")

print(MD_ER_table, "\n")


print("==================\n")

print("\nNinh Binh BASELINE EMISSIONS\n")

print("Emissions from power plant\n", NB_plant_stack.emissions().T, "\n")

print("Emissions from transport\n", NB_transport.emissions().T, "\n")

print("Emission from open field burning\n", NB_field.emissions().T, "\n")

print("-------\nNinh Binh COFIRING EMISSIONS\n")

print("Emission from power plant\n", NBCofire_plant_stack.emissions().T, "\n")

print("Emissions from transportation\n", NBCofire_transport.emissions().T, "\n")

print("Emission from open field burning\n", NBCofire_field.emissions().T, "\n")

print("-------\nNinh Binh EMISSION REDUCTION")

print(NB_ER_table, "\n")
