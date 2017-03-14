# Economic of co-firing in two power plants in Vietnam
#
# Class for business analysis
#
# (c) Minh Ha-Duong, An Ha Truong 2016
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
#
from units import time_horizon, v_zeros, USD, display_as
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
    def __init__(self, capital=0*USD):
        self.capital = capital
        self.capital.display_unit = 'kUSD'
        self.investment = display_as(v_zeros.copy()*USD, 'kUSD')
        self.investment[0] = capital

    def income(self):
        return display_as(v_zeros * USD, 'kUSD')

    def operating_expenses(self):
        return display_as(v_zeros * USD, 'kUSD')

    def amortization(self, depreciation_period):
        assert type(depreciation_period) is int, "Depreciation period not an integer"
        assert 0 < depreciation_period < time_horizon - 1, "Depreciation not in {1..timehorizon-1}"
        v_cost = v_zeros.copy()*USD
        for year in range(1, depreciation_period + 1):
            v_cost[year] = self.capital / float(depreciation_period)
        return display_as(v_cost, 'kUSD')

    def earning_before_tax(self, depreciation_period):
        earning = self.income() - self.operating_expenses() - self.amortization(depreciation_period)
        display_as(earning, 'kUSD')
        return earning

    def income_tax(self, tax_rate, depreciation_period):
        assert 0 <= tax_rate <= 1, "Tax rate not in [0, 1["
        # Allows tax credits in lossy periods
        income = tax_rate * self.earning_before_tax(depreciation_period)
        display_as(income, 'kUSD')
        return income

    def cash_out(self, tax_rate, depreciation_period):
        flow = (self.investment +
                self.operating_expenses() +
                self.income_tax(tax_rate, depreciation_period)
                )
        display_as(flow, 'kUSD')
        return flow

    def net_cash_flow(self, tax_rate, depreciation_period):
        flow = self.income() - self.cash_out(tax_rate, depreciation_period)
        display_as(flow, 'kUSD')
        return flow

    def net_present_value(self, discount_rate, tax_rate, depreciation_period):
        assert 0 <= discount_rate < 1, "Discount rate not in [0, 1["
        value = np.npv(discount_rate, self.net_cash_flow(tax_rate, depreciation_period))
        value.display_unit = 'kUSD'
        return value

    def internal_rate_of_return(self):
        pass

    def payback_period(self):
        pass

    def table(self, tax_rate=0.25, depreciation_period=10):
        t = np.array([self.income(),
                      self.investment,
                      self.amortization(depreciation_period),
                      self.operating_expenses(),
                      self.earning_before_tax(depreciation_period),
                      self.income_tax(tax_rate, depreciation_period),
                      self.cash_out(tax_rate, depreciation_period),
                      self.net_cash_flow(tax_rate, depreciation_period)
                      ]
                     )
        return t

    def pretty_table(self, discount_rate, tax_rate, depreciation_period):
        print(self.name)
        print("NPV  =", self.net_present_value(discount_rate, tax_rate, depreciation_period))
        t = self.table(tax_rate, depreciation_period)
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
