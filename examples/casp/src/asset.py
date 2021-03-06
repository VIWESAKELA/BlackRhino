#!/usr/bin/env python
# [SublimeLinter pep8-max-line-length:150]
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

# This script contains the Agent class which is later called in the Environment
# script.

import logging
import numpy as np
# ============================================================================
#
# class Asset
#
# ============================================================================

class Asset_risky(object):

    # -----------------------------------------------------------------------
    # __init__  used to automatically instantiate an agent as an object when
    # the agent class is called
    # ------------------------------------------------------------------------

    def __init__(self, firm):
        self.identifier = ""  # identifier of the specific agent
        self.state_variables = {} # stores all state_variables
        self.parameters = {} # stores all parameters
        self.prices = []
        self.firm = firm
        self.funda_values = []
        self.dividends = []
        self.set_identifier()
        self.returns=[]
        self.riskyness = []
        
        self.expected_mu = []

        self.funda_v = self.firm.dividend/self.firm.discount
        self.state_variables['mu'] = 0.0

    # -------------------------------------------------------------------------
    #

    def set_identifier(self):
        if self.firm.domicile == 0:
            self.identifier = "A"
        else:
            self.identifier = "B"

    def set_value(self):
        import numpy as np

        #Based on growth
        x = np.array([ 1 + (i) for i in self.firm.growth_results ])
        z = np.multiply(x, self.firm.dividend)
        q = np.divide( z , self.firm.discount)

        #Base it on profits
        # x = np.array([  (i) for i in self.firm.profit_results ])
        # z = np.divide( x , self.firm.discount)
        # prices_value = np.divide( z, self.firm.get_account("number_of_shares"))
        # self.prices=[prices_value]

        # self.dividends = z.tolist()
        # self.funda_values = q.tolist()
        # print "Fundamental values of " , self.identifier, self.funda_values

    def calc_exp_return(self, prev_price, exp_price, dividend):
        self.state_variables['mu'] = (exp_price-prev_price + dividend )/ prev_price
        # rate = (new_price - prev_price + self.dividends[-0)/prev_price
        rate = self.state_variables['mu']
        return rate

    def update_returns(self, environment):
        self.return_ = (self.prices[-1] - self.prices[-2] + self.firm.dividend)/self.prices[-2]
        self.returns.append(self.return_)

    def moving_average(self, n):
        history = len(self.prices)
        if history < n+1:
            return None
        else:
            moving_average = sum(self.prices[-n:]) / n
            return moving_average




    def new_price(self):
        pass

    def print_variables(self):
        print self.state_variables
        print self.parameters

    def __key__(self):
        return self.identifier

    def __eq__(self, other):
        return self.__key__() == other.__key__()

    def __hash__(self):
        return hash(self.__key__())

    def __str__(self):
        """
        Class variables: identifier, parameters, state_variables
        Local variables: ret_str, entry, value
        """
        ret_str = "  <asset identifier='" + self.identifier + "'>\n"
        for entry in self.parameters:
            value = self.parameters[entry]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                ret_str = ret_str + "    <parameter type='asset' name='" + entry + "' value='" + str(value) + "'></parameter>\n"
            else:
                raise TypeError
        for entry in self.state_variables:
            value = self.state_variables[entry]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                ret_str = ret_str + "    <variable name='" + entry + "' value='" + str(value) + "'></variable>\n"
            elif isinstance(value, list):
                ret_str = ret_str + "    <variable name='" + entry + "' value='[" + str(value[0]) + "," + str(value[1]) + \
                           "]'></variable>\n"
            else:
                raise TypeError
        ret_str = ret_str + "  </asset>\n"

        return "Share " + self.identifier + " issued by " + self.firm.identifier + "; Properties:" + ret_str

    def __getattr__(self, attr):
        if (attr in self.parameters) and (attr in self.state_variables):
            raise AttributeError('The same name exists in both parameters and state variables.')
        else:
            try:
                return self.parameters[attr]
            except:
                try:
                    return self.state_variables[attr]
                except:
                    raise AttributeError('Agent %s has no attribute "%s".' % self.identifier, attr)
    # a standard method for retrieving items from dictionaries as class attributes

    def __del__(self):
		pass

class Asset_riskfree(object):

    def __init__(self):
        self.identifier = ""  # identifier of the specific agent
        self.state_variables = {} # stores all state_variables
        self.parameters = {} # stores all parameters
        self.prices = []

    def __key__(self):
        return self.identifier

    def get_parameters_from_file(self, agent_filename, environment):
        from xml.etree import ElementTree

        try:
            xmlText = open(agent_filename).read()
            element = ElementTree.XML(xmlText)
            # we get the identifier
            self.identifier = element.attrib['identifier']

            # and then we're only interested in <parameter> fields
            element = element.findall('parameter')

            # loop over all <parameter> entries in the xml file
            for subelement in element:

                if subelement.attrib['type'] == 'parameters':
                    name = str(subelement.attrib['name'])
                    value = float(subelement.attrib['value'])
                    self.parameters[name] = value

                if subelement.attrib['type'] == 'state_variables':
                    name = str(subelement.attrib['name'])
                    value = float(subelement.attrib['value'])
                    self.state_variables[name] = value

        except:
            logging.error("    ERROR: %s could not be parsed", agent_filename)

        self.state_variables["r_f"] = environment.variable_parameters['r_f']


    def __str__(self):
        """
        Class variables: identifier, parameters, state_variables
        Local variables: ret_str, entry, value
        """
        ret_str = "  <asset identifier='" + self.identifier + "'>\n"
        for entry in self.parameters:
            value = self.parameters[entry]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                ret_str = ret_str + "    <parameter type='asset' name='" + entry + "' value='" + str(value) + "'></parameter>\n"
            else:
                raise TypeError
        for entry in self.state_variables:
            value = self.state_variables[entry]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
                ret_str = ret_str + "    <variable name='" + entry + "' value='" + str(value) + "'></variable>\n"
            elif isinstance(value, list):
                ret_str = ret_str + "    <variable name='" + entry + "' value='[" + str(value[0]) + "," + str(value[1]) + \
                           "]'></variable>\n"
            else:
                raise TypeError
        ret_str = ret_str + "  </asset>\n"

        return "Bond " + self.identifier + " issued by Government "  "; Properties:" + ret_str


    def __getattr__(self, attr):
        if (attr in self.parameters) and (attr in self.state_variables):
            raise AttributeError('The same name exists in both parameters and state variables.')
        else:
            try:
                return self.parameters[attr]
            except:
                try:
                    return self.state_variables[attr]
                except:
                    raise AttributeError('Agent %s has no attribute "%s".' % self.identifier, attr)
