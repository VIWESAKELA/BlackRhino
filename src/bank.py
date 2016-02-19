#!/usr/bin/env python
# [SublimeLinter pep8-max-line-length:300]
# -*- coding: utf-8 -*-

"""
black_rhino is a multi-agent simulator for financial network analysis
Copyright (C) 2016 Co-Pierre Georg (co-pierre.georg@keble.ox.ac.uk)
Pawel Fiedor (pawel@fiedor.eu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from abm_template.src.baseagent import BaseAgent

# ============================================================================
#
# class Bank
#
# ============================================================================


class Bank(BaseAgent):
    #
    #
    # VARIABLES
    #
    #
    identifier = ""
    parameters = {}
    state_variables = {}
    accounts = []  # all accounts of a bank

    parameters["active"] = 0

#
#
# CODE
#
#

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, _value):
        """
        Class variables: identifier
        Local variables: _identifier
        """
        super(Bank, self).set_identifier(_value)

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, _value):
        """
        Class variables: parameters
        Local variables: _params
        """
        super(Bank, self).set_parameters(_value)

    def get_state_variables(self):
        return self.state_variables

    def set_state_variables(self, _value):
        """
        Class variables: state_variables
        Local variables: _variables
        """
        super(Bank, self).set_state_variables(_value)

    def append_parameters(self, _value):
        super(Bank, self).append_parameters(_value)

    def append_state_variables(self, _value):
        super(Bank, self).append_state_variables(_value)

    # -------------------------------------------------------------------------
    # functions needed to make Bank() hashable
    # -------------------------------------------------------------------------
    def __key__(self):
        return self.identifier

    def __eq__(self, other):
        return self.__key__() == other.__key__()

    def __hash__(self):
        return hash(self.__key__())
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # __init__
    # -------------------------------------------------------------------------
    def __init__(self):
        self.accounts = []  # clear transactions when bank is initialized
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # __del__
    # -------------------------------------------------------------------------
    def __del__(self):
        pass
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # __str__
    # -------------------------------------------------------------------------
    def __str__(self):
        text = "<bank identifier='" + self.identifier + "'>\n"
        text += "    <value name='active' value='" + str(self.parameters["active"]) + "'></value>\n"
        text += "    <transactions>\n"
        for transaction in self.accounts:
            text += transaction.write_transaction()
        text += "    </transactions>\n"
        text += "</bank>\n"

        return text
    # ------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_parameters_from_file
    # -------------------------------------------------------------------------
    def get_parameters_from_file(self,  bankFilename, environment):
        super(Bank, self).get_parameters_from_file(bankFilename, environment)
    # ------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # check_consistency
    # -------------------------------------------------------------------------
    def check_consistency(self):
        _assets = ["LOAN", "MONEY"]
        _liabilities = ["DEPOSIT"]
        return super(Bank, self).check_consistency(_assets, _liabilities)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_account
    # -------------------------------------------------------------------------
    def get_account(self,  _type):
        return super(Bank, self).get_account(_type)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # get_account_num_transactions
    # -------------------------------------------------------------------------
    def get_account_num_transactions(self,  _type):  # returns the number of transactions in a given account
        return super(Bank, self).get_account_num_transactions(_type)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # add_transaction
    # -------------------------------------------------------------------------
    def add_transaction(self,  type,  fromID,  toID,  value,  interest,  maturity, timeOfDefault):
        from src.transaction import Transaction
        transaction = Transaction()
        transaction.this_transaction(type,  fromID,  toID,  value,  interest,  maturity,  timeOfDefault)
        self.accounts.append(transaction)
        del transaction
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # clear_accounts
    # -------------------------------------------------------------------------
    def clear_accounts(self):
        super(Bank, self).clear_accounts()
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # purge_accounts
    # -------------------------------------------------------------------------
    def purge_accounts(self):
        super(Bank, self).purge_accounts()
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # initialize_standard_bank
    #
    # this routine initializes a bank with a standard balance sheet,
    # which can be used to make the tests more handy
    # -------------------------------------------------------------------------
    def initialize_standard_bank(self, environment):
        from src.transaction import Transaction

        self.identifier = "standard_bank_id"

        # deposits - we get the first household from the list of households
        # if there are no households it will be a blank which is fine for testing
        value = 250.0
        transaction = Transaction()
        transaction.this_transaction("DEPOSIT",  environment.households[0:1][0],  self.identifier,  value,  environment.static_parameters["interest_rate_deposits"],  0, -1)
        self.accounts.append(transaction)
        del transaction

        # money - cash and equivalents
        value = 100.0
        transaction = Transaction()
        transaction.this_transaction("MONEY",  self.identifier, self.identifier,  value,  0,  0, -1)
        self.accounts.append(transaction)
        del transaction

        # loans - we get the first firm from the list of firms
        # if there are no firms it will be a blank which is fine for testing
        value = 150.0
        transaction = Transaction()
        transaction.this_transaction("LOAN",  self.identifier, environment.firms[0:1][0],  value,  environment.static_parameters["interest_rate_loans"],  0, -1)
        self.accounts.append(transaction)
        del transaction

    # -------------------------------------------------------------------------
