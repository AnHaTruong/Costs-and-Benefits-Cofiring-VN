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

MongDuong1.Commissioning     =  2015    # year
MongDuong1.BoilerTechnology  =  "CFB"
MongDuong1.Capacity          =  1080    # MW
MongDuong1.Generation        =  6500    # GWh/yr
MongDuong1.CoalConsumption   =     2.75 # Mt/yr
MongDuong1.CoalHeatValue     =    19.4  # Mj/kg
MongDuong1.PlantEfficiency   =   38.84  # percent
MongDuong1.BoilerEfficiency  =   87.03  # percent

NinhBinh = PowerPlant()

NinhBinh.Commissioning     =  1974    # year
NinhBinh.BoilerTechnology  =  "PC"
NinhBinh.Capacity          =   100    # MW
NinhBinh.Generation        =   750    # GWh/yr
NinhBinh.CoalConsumption   =     0.42 # Mt/yr
NinhBinh.CoalHeatValue     =    25.3  # Mj/kg
NinhBinh.PlantEfficiency   =   21.77  # percent
NinhBinh.BoilerEfficiency  =   81.61  # percent

MongDuong1.CapitalCost     =     50       # USD/kW
MongDuong1.StrawRequired   = 259107       # ton/year
MongDuong1.CoalPrice       =     52.69    # USD/ton
MongDuong1.StrawUnitCost   =     41.31    # USD/ton
MongDuong1.FixOMCost       =     32.34    # USD/kW.year
MongDuong1.VariableOMCost  =      0.6     # UScent/kWh

NinhBinh.CapitalCost     =     100       # USD/kW
NinhBinh.StrawRequired   =   53362       # ton/year
NinhBinh.CoalPrice       =     83.83    # USD/ton
NinhBinh.StrawUnitCost   =     38.15    # USD/ton
NinhBinh.FixOMCost       =     32.34    # USD/kW.year
NinhBinh.VariableOMCost  =      0.6     # UScent/kWh