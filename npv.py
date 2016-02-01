# Economic of co-firing in two power plants in Vietnam
#
#  NPV assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

TimeHorizon    =   20         # years
DiscountRate   =    8.78/100  # per year

def npv(CashFlow):
    value = 0
    for t in range(TimeHorizon+1):
        value += CashFlow(t) / (1+DiscountRate)**t
    return value
