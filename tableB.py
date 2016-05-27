# Economic of co-firing in two power plants in Vietnam
#
# Jobs creation
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
""" Print the result of farmer extra income assessment from farmerincome.py"""

from parameters import MongDuong1, NinhBinh

from farmerincome import farmer_income, bm_sell_revenue, total_income_benefit

print('')
head = '{:40}' + '{:28}' + '{:15}'
row = '{:30}' + '{:23.5f}'*2

print (head.format(' ', 'Mong Duong 1', 'Ninh Binh'))

print (row.format('biomass sell revenue',
                  bm_sell_revenue(MongDuong1),
                  bm_sell_revenue(NinhBinh)
                  )
      )

print (row.format('farmer income per ha',
                  farmer_income(MongDuong1),
                  farmer_income(NinhBinh)
                  )
      )

print (row.format('total benefit from farmers extra income',
                  total_income_benefit(MongDuong1),
                  total_income_benefit(NinhBinh)
                  )
      )
