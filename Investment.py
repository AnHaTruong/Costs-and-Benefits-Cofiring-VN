# Economic of co-firing in two power plants in Vietnam
#
# Class for business analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from init import time_horizon, v_zeros, v_after_invest, USD, display_as
import natu.numpy as np
import pandas as pd


class Investment:
    """An investment of capital made in period 0,
        There are income, operating expenses and taxes in subsequent periods
        Taxes account for linear amortization of the capital starting period 1
        No salvage value
       Virtual class,
        descendent class should redefine  income()  and  operating_expense() to
           return a vector of quantities of size time_horizon+1
           which has the display unit set to kUSD
    """
    def __init__(self, capital=0 * USD):
        self.capital = display_as(capital, 'kUSD')

    def income(self, feedin_tariff):
        return display_as(v_zeros * USD, 'kUSD')

    def investment(self):
        """Multi year investment not tested"""
        v_invest = 1 - v_after_invest
        return display_as(v_invest * self.capital / sum(v_invest), 'kUSD')

    def operating_expenses(self):
        return display_as(v_zeros * USD, 'kUSD')

    def amortization(self, depreciation_period):
        assert type(depreciation_period) is int, "Depreciation period not an integer"
        assert 0 < depreciation_period < time_horizon - 1, "Depreciation not in {1..timehorizon-2}"
        v_cost = v_zeros.copy() * USD
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.capital / float(depreciation_period)
        return display_as(v_cost, 'kUSD')

    def earning_before_tax(self, feedin_tariff, depreciation_period):
        earning = (self.income(feedin_tariff)
                   - self.operating_expenses()
                   - self.amortization(depreciation_period))
        return display_as(earning, 'kUSD')

    def income_tax(self, feedin_tariff, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        income = tax_rate * self.earning_before_tax(feedin_tariff, depreciation_period)
        return display_as(income, 'kUSD')

    def cash_out(self, feedin_tariff, tax_rate, depreciation_period):
        flow = (self.investment()
                + self.operating_expenses()
                + self.income_tax(feedin_tariff, tax_rate, depreciation_period))
        return display_as(flow, 'kUSD')

    def net_cash_flow(self, feedin_tariff, tax_rate, depreciation_period):
        flow = (self.income(feedin_tariff)
                - self.cash_out(feedin_tariff, tax_rate, depreciation_period))
        return display_as(flow, 'kUSD')

    def net_present_value(self, feedin_tariff, discount_rate, tax_rate, depreciation_period):
        assert 0 <= discount_rate < 1, "Discount rate not in [0, 1["
        value = np.npv(discount_rate,
                       self.net_cash_flow(feedin_tariff, tax_rate, depreciation_period))
        return display_as(value, 'kUSD')

    def internal_rate_of_return(self):
        pass

    def payback_period(self):
        pass

    def table(self, feedin_tariff, tax_rate=0.25, depreciation_period=10):
        t = np.array([self.income(feedin_tariff),
                      self.investment(),
                      self.amortization(depreciation_period),
                      self.operating_expenses(),
                      self.earning_before_tax(feedin_tariff, depreciation_period),
                      self.income_tax(feedin_tariff, tax_rate, depreciation_period),
                      self.cash_out(feedin_tariff, tax_rate, depreciation_period),
                      self.net_cash_flow(feedin_tariff, tax_rate, depreciation_period)
                      ]
                     )
        return t

    def pretty_table(self, feedin_tariff, discount_rate, tax_rate, depreciation_period):
        print(self.name)
        print("NPV  =", self.net_present_value(feedin_tariff,
                                               discount_rate,
                                               tax_rate,
                                               depreciation_period))
        t = self.table(feedin_tariff, tax_rate, depreciation_period)
        t = np.transpose(t)
        labels = ["Income",
                  "Investment",
                  "Amortization",
                  "Op. Expense",
                  "Earn. B. Tax",
                  "Income tax",
                  "Cash out",
                  "Net cashflow"
                  ]
        t = pd.DataFrame(t, columns=labels)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 150)
        print(t)
        return t
