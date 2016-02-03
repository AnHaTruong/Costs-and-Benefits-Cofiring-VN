# Economic of co-firing in two power plants in Vietnam
#
#  NPV assessment
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

from parameters import TimeHorizon,DiscountRate,BiomassRatio,ElectricityTariffUSD,GWtokW

def npv(CashFlow):
    value = 0
    for t in range(TimeHorizon+1):
        value += CashFlow(t) / (1+DiscountRate)**t
    return value

#electricity sale refers to line 98 in Excel sheet
# This is only for the project
def ElectricitySaleQuantity(plant,t):
    if t==0:
        return 0
    else: 
        return plant.Generation*GWtokW * BiomassRatio

#Excel line 99 and 102
# This is only for the project
def CashInflow(plant, t):
    return ElectricitySaleQuantity(plant,t) * ElectricityTariffUSD

# This is only for the project
def CashOutflow(plant, t):
    return TotalCapitalCost(plant,t) + FuelCost(plant,t) + OperationMaintenanceCost(plant,t) + IncomeTax(plant,t)

# We assume the plant is paid for coal at capacity design.
# this is only extra capital cost for the biomass co-firing  ??? Total
# This is only for the project
def TotalCapitalCost(plant,t):
    if t==0:
        return plant.Capacity*MWtokW * plant.CapitalCost * plant.BiomassRatio  
    else:
        return 0

def FuelCost(plant,t):
    BiomassCost = plant.BiomassRequired * plant.BiomassUnitCost  
    return BiomassCost    

def OperationMaintenanceCost(plant,t):
    FixedOMCost = plant.Capacity*MWtokW * plant.FixOMCost  * plant.BiomassRatio
    VaribleOMCost = ElectricitySaleQuantity * plant.VariableOMCost
    return FixedOMCost + VariableOMCost

def IncomeTax(plant,t):           # ??? name it Corporate tax 
    return TaxRate * EarnBeforeTax(plant,t)

def EarnBeforeTax(plant,t):              # ??? Amortizations
    return CashInflow(plant,t) - FuelCost(plant,t) - OperationMaintenanceCost(plant,t)

def NetCashFlow(plant,t):
    return CashInflow(plant,t) - CashOutflow(plant,t)