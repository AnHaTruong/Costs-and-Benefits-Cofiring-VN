# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2019
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Define the class  System  used to instantiate a run of the model."""
from collections import namedtuple

from pandas import Series, DataFrame, set_option, concat
from natu.numpy import npv, sum as np_sum

from model.utils import year_1, display_as, safe_divide, t
from model.powerplant import PowerPlant, CofiringPlant
from model.farmer import Farmer
from model.reseller import Reseller

Price = namedtuple('Price',
                   'biomass_plantgate, biomass_fieldside, coal, electricity')

MiningParameter = namedtuple('MiningParameter',
                             'productivity_surface, productivity_underground, wage_mining')


# We should pass the parameters as an object
#pylint: disable=too-many-instance-attributes
#
# Refectoring needed:
# We should split the class into a  System  that knows only about one type of plant,
# and a comparison class that holds a system_ex_ante and a system_ex_post
#pylint: disable=R0904
class System:
    """The system model of the cofiring economic sector.

    Instance variables: plant, cofiring plant, supply_chain, reseller, farmer.
    The class is designed immutable, don't change the members after initialization.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, plant_parameter, cofire_parameter, supply_chain_potential, price,
                 farm_parameter, transport_parameter, mining_parameter, emission_factor):
        """Instantiate the system actors."""
        self.plant = PowerPlant(plant_parameter, emission_factor)
        self.cofiring_plant = CofiringPlant(plant_parameter, cofire_parameter, emission_factor)
        self.supply_chain = supply_chain_potential.fit(self.cofiring_plant.biomass_used[1])
        self.farmer = Farmer(self.supply_chain, farm_parameter, emission_factor)
        self.reseller = Reseller(self.supply_chain, transport_parameter, emission_factor)
        self.mining_parameter = mining_parameter
        self.clear_market(price)

    def clear_market(self, price):
        """Realize the payments between actors."""
        self.price = price

        electricity_sales = self.plant.power_generation * price.electricity
        display_as(electricity_sales, 'kUSD')

        self.plant.revenue = electricity_sales
        self.plant.coal_cost = self.plant.coal_used * price.coal

        self.cofiring_plant.revenue = electricity_sales
        self.cofiring_plant.coal_cost = self.cofiring_plant.coal_used * price.coal

        # Transaction  at the plant gate
        payment_plantgate = self.cofiring_plant.biomass_used * price.biomass_plantgate
        display_as(payment_plantgate, "kUSD")
        self.cofiring_plant.biomass_cost = self.reseller.revenue = payment_plantgate

        # Transaction  at the field side
        payment_fieldside = self.cofiring_plant.biomass_used * price.biomass_fieldside
        display_as(payment_fieldside, "kUSD")
        self.farmer.revenue = self.reseller.merchandise = payment_fieldside

    @property
    def transport_cost_per_t(self):
        """Return technical cost to transport the straw, including labor, fuel and truck rental."""
        return safe_divide(self.reseller.operating_expenses(), self.cofiring_plant.biomass_used)

    @property
    def labor(self):
        """Return total work time created from co-firing."""
        time = (self.farmer.labor()
                + self.reseller.labor()
                + self.cofiring_plant.biomass_om_work()
                - self.coal_work_lost)
        return display_as(time, 'hr')

    @property
    def wages(self):
        """Return total benefit from job creation from biomass co-firing."""
        amount = (self.farmer.labor_cost()
                  + self.reseller.labor_cost()
                  + self.cofiring_plant.biomass_om_wages()
                  - self.coal_wages_lost)
        return display_as(amount, 'kUSD')

    def wages_npv(self, discount_rate):
        amount = npv(discount_rate, self.wages)
        return display_as(amount, 'kUSD')

    @property
    def coal_saved(self):
        mass = self.plant.coal_used - self.cofiring_plant.coal_used
        return display_as(mass, 'kt')

    @property
    def coal_work_lost(self):
        time = self.coal_saved / self.mining_parameter.productivity_underground
        return display_as(time, "hr")

    @property
    def coal_wages_lost(self):
        value = self.coal_work_lost * self.mining_parameter.wage_mining
        return display_as(value, 'kUSD')

    def emissions_baseline(self):
        """Tabulate system atmospheric emissions in year 1 ex ante (no cofiring)."""
        baseline = DataFrame(columns=['CO2', 'NOx', 'PM10', 'SO2'])
        baseline = baseline.append(year_1(self.plant.emissions()))
        baseline = baseline.append(year_1(self.plant.coal_reseller().emissions()))
        baseline = baseline.append(year_1(self.farmer.emissions_exante))
        baseline.loc["Total"] = baseline.sum()
        baseline.loc["Total_plant"] = baseline.iloc[0]
        baseline.loc["Total_transport"] = baseline.iloc[1]
        baseline.loc["Total_field"] = baseline.iloc[2]
        return baseline

    def emissions_cofiring(self):
        """Tabulate system atmospheric emissions in year 1 ex post (with cofiring)."""
        cofiring = DataFrame(columns=['CO2', 'NOx', 'PM10', 'SO2'])
        cofiring = cofiring.append(year_1(self.cofiring_plant.emissions()))
        cofiring = cofiring.append(year_1(self.cofiring_plant.coal_reseller().emissions()))
        cofiring = cofiring.append(year_1(self.farmer.emissions()))
        cofiring = cofiring.append(year_1(self.reseller.emissions()))
        cofiring.loc["Total"] = cofiring.sum()
        cofiring.loc["Total_plant"] = cofiring.iloc[0] + cofiring.iloc[1]
        cofiring.loc["Total_transport"] = cofiring.iloc[2] + cofiring.iloc[4]
        cofiring.loc["Total_field"] = cofiring.iloc[3]
        return cofiring

    def emissions_exante(self):
        """Tabulate atmospheric emissions ex ante.

        Return a dataframe of time series, indexed by segment and pollutant.
        """
        plant_emissions = self.plant.emissions(total=True)['Total']
        ship_coal_emissions = self.plant.coal_reseller().emissions(total=True)['Total']
        field_emissions = self.farmer.emissions_exante['Straw']
        transport_emissions = field_emissions * 0  # No logistics
        total_emissions = plant_emissions + ship_coal_emissions + field_emissions
        return DataFrame(
            [plant_emissions, ship_coal_emissions, transport_emissions, field_emissions,
             total_emissions],
            index=['Plant', 'Ship coal', 'Transport', 'Field', 'Total'])

    def emissions_expost(self):
        """Tabulate atmospheric emissions ex post.

        Return a dataframe of time series, indexed by segment and pollutant.
        """
        plant_emissions = self.cofiring_plant.emissions(total=True)['Total']
        ship_coal_emissions = self.cofiring_plant.coal_reseller().emissions(total=True)['Total']
        transport_emissions = self.reseller.emissions(total=True)['Total']
        field_emissions = self.farmer.emissions(total=True)['Total']
        total_emissions = (
            plant_emissions
            + ship_coal_emissions
            + transport_emissions
            + field_emissions)
        return DataFrame(
            [plant_emissions, ship_coal_emissions, transport_emissions, field_emissions,
             total_emissions],
            index=['Plant', 'Ship coal', 'Transport', 'Field', 'Total'])

    def emissions_reduction(self):
        """Tabulate atmospheric emissions reductions.

        Return a dataframe of time series, indexed by segment and pollutant.
        """
        reduction = self.emissions_exante() - self.emissions_expost()
        is_null_year0 = reduction.applymap(lambda sequence: sequence[0] == 0 * t)
        assert is_null_year0.all(axis=None), "Expecting zero emission reduction in year 0"
        return reduction

    def emissions_reduction_benefit(self, external_cost):
        """Tabulate external benefits of reducing atmospheric emissions from cofiring.

        Return a dataframe of time series, indexed by segment and pollutant.
        """
        baseline = self.emissions_exante().loc["Total"]
        reduction = self.emissions_reduction().loc["Total"]
        relative = reduction / baseline
        benefit = reduction * external_cost
        for pollutant in benefit:
            display_as(pollutant, 'kUSD')
        for pollutant in external_cost:
            display_as(pollutant, 'USD / t')
        return DataFrame(
            [baseline, reduction, relative, benefit],
            index=["Baseline", "Reduction", "Relative reduction", "Value"])

    def coal_saved_benefits(self, coal_import_price):
        """Tabulate the quantity and value of coal saved by cofiring."""
        baseline = self.plant.coal_used
        reduction = self.coal_saved
        relative = reduction / baseline
        benefit = reduction * coal_import_price
        display_as(benefit, 'MUSD')
        return DataFrame(
            [baseline, reduction, relative, benefit],
            index=["Baseline", "Reduction", "Relative reduction", "Value"])

    def mitigation_npv(self, discount_rate, external_cost):
        df = self.emissions_reduction_benefit(external_cost)
        annual_mitigation_value = df.loc['Value', 'CO2']
        value = npv(discount_rate, annual_mitigation_value)
        return display_as(value, 'kUSD')

    def health_npv(self, discount_rate, external_cost):
        df = self.emissions_reduction_benefit(external_cost)
        annual_health_benefit = df.loc['Value'].drop('CO2').sum()
        value = npv(discount_rate, annual_health_benefit)
        return display_as(value, 'kUSD')

    def parameters_table(self):
        """Tabulate arguments defining the system, except supply chain. Return a Pandas Series."""
        set_option('display.max_colwidth', 80)
        legend_a = Series("----------", index=["*** Farmer ***"])
        a = self.farmer.parameters_table()
        legend_b = Series("----------", index=["*** Reseller***"])
        b = self.reseller.parameters_table()
        legend_c = Series("----------", index=["*** Cofiring plant ***"])
        c = self.cofiring_plant.parameters_table()
        legend_d = Series("----------", index=["*** Mining ***"])
        d = Series(self.mining_parameter, self.mining_parameter._fields)
        display_as(d.loc['wage_mining'], "USD / hr")
        legend_e = Series("----------", index=["*** Prices ***"])
        e = Series(self.price, self.price._fields)
        display_as(e.loc['biomass_plantgate'], "USD / t")
        display_as(e.loc['biomass_fieldside'], "USD / t")
        display_as(e.loc['coal'], "USD / t")
        display_as(e.loc['electricity'], "USD / kWh")
        return concat([legend_c, c, legend_a, a, legend_b, b, legend_d, d, legend_e, e])

    def benefits(self, discount_rate, external_cost):
        """Tabulate the present value of various benefits from co-firing."""
        table = ['']
        table.append(self.cofiring_plant.name)
        table.append('-------------------')
        row2 = '{:30}' + '{:20.0f}'
        table.append(row2.format('Health', self.health_npv(discount_rate, external_cost)))
        table.append(row2.format('Emission reduction',
                                 self.mitigation_npv(discount_rate, external_cost)))
        table.append(row2.format('Wages', self.wages_npv(discount_rate)))
        table.append(row2.format('Farmer earnings before tax',
                                 self.farmer.net_present_value(discount_rate)))
        table.append(row2.format('Trader earnings before tax',
                                 self.reseller.net_present_value(discount_rate)))
        return '\n'.join(table)

    def plant_npv_cash_change(self, discount_rate, tax_rate, depreciation_period):
        """Return the NPV change table for the power plant.

        Cofiring profit is positive if its benefits (reducing the operating expenses)
        exceeds its costs (the investment).
        """
        name = self.plant.name
        exante = self.plant.npv_cash(discount_rate, tax_rate, depreciation_period, name)
        expost = self.cofiring_plant.npv_cash(discount_rate, tax_rate, depreciation_period, name)
        return expost - exante

    def plant_npv_opex_change(self, discount_rate):
        """Return the Operating expenses changes for the power plant.

        Ex post compared to ex ante:
            the coal costs are lower
            the biomass costs are higher
            the total Operations and Maintenance are higher
        and if the biomass is cheap enough, then the operating expenses decrease.
        """
        name = self.plant.name
        npv_opex_exante = self.plant.npv_opex(discount_rate, name)
        table = self.cofiring_plant.npv_opex(discount_rate, name)
        table.loc['Fuel cost, coal'] -= npv_opex_exante.loc['Fuel cost, coal']
        table.loc['O&M, coal'] -= npv_opex_exante.loc['Operation & Maintenance']
        table.loc['= Operating expenses'] -= npv_opex_exante.loc['= Operating expenses']
        return table

    def table_business_value(self, discount_rate):
        """Tabulate cofiring business value:  technical costs vs. value of coal saved."""
        data = [
            npv(discount_rate, self.farmer.operating_expenses()),
            npv(discount_rate, self.reseller.operating_expenses()),
            npv(discount_rate, self.cofiring_plant.investment())]

        table_opex = self.plant_npv_opex_change(discount_rate)
        extra_OM = table_opex.loc['O&M, coal'] + table_opex.loc['O&M, biomass']
        data.append(display_as(extra_OM, 'kUSD'))

        technical_cost = np_sum(data)
        data.append(technical_cost)

        coal_saved = npv(discount_rate, self.coal_saved)
        coal_price = display_as(self.price.coal, "USD/t")
        savings = display_as(coal_saved * coal_price, "kUSD")
        data.append(coal_saved)
        data.append(coal_price)
        data.append(savings)

        data.append(savings - technical_cost)

        index = [
            "Farmer opex",
            "Reseller opex",
            "Investment",
            "Extra O&M",
            "Total technical costs",
            "Coal saved",
            "Coal price",
            "Value of coal saved",
            "Business value of cofiring"]
        table = Series(data, index=index)
        table.name = self.plant.name
        return table

    # Code really smell, will change result to DataFrame now.
    # pylint: disable=too-many-locals
    def job_changes(self):
        """Tabulate the number of full time equivalent (FTE) jobs created/destroyed by cofiring."""
        cols = '{:25}{:12.1f}'
        cols2 = '{:25}{:12.1f}{:12.1f}'

        lines = ['Benefit from job creation: ' + self.plant.name + '\n']

        row7 = self.farmer.labor()[1]
        row1 = self.farmer.labor_cost()[1]
        row8 = self.reseller.driving_work()[1]
        row2 = self.reseller.driving_wages()[1]
        row11 = self.reseller.loading_work()[1]
        row12 = self.reseller.loading_wages()[1]
        row9 = self.cofiring_plant.biomass_om_work()[1]
        row3 = self.cofiring_plant.biomass_om_wages()[1]
        row6 = - self.coal_work_lost[1]
        row5 = - self.coal_wages_lost[1]
        row10 = self.labor[1]
        row4 = self.wages[1]

        display_as(row6, 'FTE')
        display_as(row7, 'FTE')
        display_as(row8, 'FTE')
        display_as(row9, 'FTE')
        display_as(row10, 'FTE')
        display_as(row11, 'FTE')

        lines.append(cols2.format('Biomass collection', row7, row1))
        lines.append(cols2.format('Biomass transportation', row8, row2))
        lines.append(cols2.format('Biomass loading', row11, row12))
        lines.append(cols2.format('O&M', row9, row3))
        lines.append(cols2.format('Mining', row6, row5))
        lines.append(cols2.format('Total', row10, row4))
        lines.append('')
        lines.append(cols.format('Area collected', self.supply_chain.area()))
        lines.append(cols.format('Collection radius', self.supply_chain.collection_radius()))
        lines.append(cols.format('Maximum transport time', self.reseller.max_trip_time()))
        lines.append(cols.format('Number of truck trips', self.reseller.truck_trips[1]))
        lines.append('')
        lines.append('Mining job lost from co-firing at ' + self.plant.name + '\n')
        lines.append(cols.format('Coal saved', self.coal_saved[1]))
        lines.append(cols.format('Productivity', self.mining_parameter.productivity_underground))
        lines.append(cols.format('Job lost', self.coal_work_lost[1]))
        lines.append(cols.format('Job lost', display_as(self.coal_work_lost[1], "FTE")))
        lines.append(cols.format('Wage', display_as(self.mining_parameter.wage_mining, "USD/hr")))
        lines.append(cols.format('Wage lost', self.coal_wages_lost[1]))
        return '\n'.join(lines)
