# Economic of co-firing in two power plants in Vietnam
#
#  Plant parameters
#
# (c) Minh Ha-Duong, An Ha Truong   2016
#     minh.haduong@gmail.com
#     Creative Commons Attribution-ShareAlike 4.0 International
#
#

class PowerPlant:
    pass

MongDuong1 = PowerPlant()

MongDuong1.Commissioning         =  2015    # year
MongDuong1.BoilerTechnology      =  "CFB"
MongDuong1.Capacity              =  1080    # MW
MongDuong1.Generation            =  6500    # GWh/yr
MongDuong1.CoalHeatValue         =    19.4  # Mj/kg
MongDuong1.BaseCoalConsumption   =     2.75 # Mt/yr
MongDuong1.BasePlantEfficiency   =   38.84  # percent
MongDuong1.BaseBoilerEfficiency  =   87.03  # percent

NinhBinh = PowerPlant()

NinhBinh.Commissioning         =  1974    # year
NinhBinh.BoilerTechnology      =  "PC"
NinhBinh.Capacity              =   100    # MW
NinhBinh.Generation            =   750    # GWh/yr
NinhBinh.CoalHeatValue         =    25.3  # Mj/kg
NinhBinh.BaseCoalConsumption   =     0.42 # Mt/yr
NinhBinh.BasePlantEfficiency   =   21.77  # percent
NinhBinh.BaseBoilerEfficiency  =   81.61  # percent

MongDuong1.CapitalCost         =     50       # USD/kW
MongDuong1.BiomassRequired     = 259107       # ton/year    Computed using annex 2 assuming 5% co-firing 
MongDuong1.CoalPrice           =     52.69    # USD/ton
MongDuong1.BiomassUnitCost     =     41.31    # USD/ton     Computed using annex 2 assuming 5% co-firing 
MongDuong1.FixOMCost           =     32.34    # USD/kW.year
MongDuong1.VariableOMCost      =      0.6     # UScent/kWh
  
NinhBinh.CapitalCost           =     100       # USD/kW
NinhBinh.BiomassRequired       =   53362       # ton/year    Computed using annex 2 assuming 5% co-firing 
NinhBinh.CoalPrice             =     83.83     # USD/ton
NinhBinh.BiomassUnitCost       =     38.15     # USD/ton     Computed using annex 2 assuming 5% co-firing 
NinhBinh.FixOMCost             =     32.34     # USD/kW.year
NinhBinh.VariableOMCost        =      0.6      # UScent/kWh

ElectricityTariffVND           =      1158.1   # VND/kWh
BiomassRatio                   =      0.05    
TimeHorizon                    =     20         # years
DiscountRate                   =    8.78/100  # per year
TaxRate                        =      0.25      # Corporate tax in Vietnam
MWtokW                         =   1000         # conversion factor
GWtokW                         = 1000000        # conversion factor
ExchangeRate                   = 21473          # VND/USD
ElectricityTariffUSD           = ElectricityTariffVND/ExchangeRate