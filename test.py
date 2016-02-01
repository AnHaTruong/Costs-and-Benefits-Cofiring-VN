# Economic of co-firing in two power plants in Vietnam
#
#  Tests
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

from parameters import NinhBinh,MongDuong1

print(MongDuong1.Capacity)
print(NinhBinh.Capacity)

print

from npv import npv,TimeHorizon,DiscountRate

print(TimeHorizon)
print(DiscountRate)

print

print("Tests for NPV function")
print

print("Null cash flow")
def nocash(t):
    return 0
print(npv(nocash))
if npv(nocash) == 0:
    print("OK")
else:
    print("ERROR: the null cash flow should have null NPV")

print

print("Unit cash flow")
def unitcash(t):
    return 1
print(repr(npv(unitcash)))
CommonRatio = 1/(1+DiscountRate)
SumOfGeometricSequence = (1 - CommonRatio**(TimeHorizon+1)) / (1 - CommonRatio)
print(repr(SumOfGeometricSequence))
if npv(unitcash) - SumOfGeometricSequence < 1E-12:
    print("OK")
else:
    print("ERROR: NPV of the unit cash flow is wrong")



