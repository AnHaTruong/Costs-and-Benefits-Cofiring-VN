# Economic of co-firing in two power plants in Vietnam
#
#  Levelized cost of electricity(LCOE) assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#
"""test for the LCOE funcction in file lcoe.py"""

from parameters import MongDuong1, NinhBinh

from LCOE import cap_rec_factor, lcoe
from LCOE import lcoe_cap_return, lcoe_fix_om, lcoe_bm_cost, lcoe_variable_om


print('')
print('capacity recovery factor', (cap_rec_factor()))

print('')
head = '{:22}' + '{:15}'*2
row = '{:22}' + '{:30.5f}'*2

print (head.format(' ', 'Mong Duong 1', 'Ninh Binh'))

print (row.format('biomass cost',
                  MongDuong1.biomass_unit_cost,
                  NinhBinh.biomass_unit_cost
                  )
      )

print (row.format('heat rate',
                  MongDuong1.heat_rate,
                  NinhBinh.heat_rate
                  )
       )

print (row.format('capital cost',
                  MongDuong1.capital_cost,
                  NinhBinh.capital_cost
                  )
       )

print (row.format('fix O&M',
                  MongDuong1.fix_om_cost,
                  NinhBinh.fix_om_cost
                  )
       )

#print (row.format('biomass cost per MJ',
#                  bm_unit_cost_mj(MongDuong1),
#                  bm_unit_cost_mj(NinhBinh)
#                  )
#      )

print (row.format('lcoe capital return',
                  lcoe_cap_return(MongDuong1),
                  lcoe_cap_return(NinhBinh)
                  )
       )

print (row.format('lcoe fix OM',
                  lcoe_fix_om(MongDuong1),
                  lcoe_fix_om(NinhBinh)
                  )
      )

print (row.format('lcoe biomass cost',
                  lcoe_bm_cost(MongDuong1),
                  lcoe_bm_cost(NinhBinh)
                  )
      )

print (row.format('lcoe variable OM',
                  lcoe_variable_om(MongDuong1),
                  lcoe_variable_om(NinhBinh)
                  )
      )

print (row.format('LCOE', lcoe(MongDuong1), lcoe(NinhBinh)))
