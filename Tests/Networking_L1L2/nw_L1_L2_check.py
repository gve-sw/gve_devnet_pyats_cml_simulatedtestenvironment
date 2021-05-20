"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

#!/bin/env python

# To get a logger for the script
import logging

# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from ats import aetest
from ats.log.utils import banner

# Genie Imports
from genie.conf import Genie
from genie.abstract import Lookup

# import the genie libs
from genie.libs import ops # noqa

# Get your logger for your script
log = logging.getLogger(__name__)



import json
import test_params


###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    # CommonSetup have subsection.
    # You can have 1 to as many subsection as wanted

    # Connect to each device in the testbed
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(
                "Connect to device '{d}'".format(d=device.name)))
            try:
                device.connect()
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)


###################################################################
#                     TESTCASES SECTION                           #
###################################################################

class nw_L1_L2(aetest.Testcase):
    """ This is user Testcases section """

    @ aetest.test
    def check_interface_status(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering Interface Information from {}".format(
                    dev.name)))
                output = dev.parse('show ip interface brief')
                for interface in output["interface"]:
                    mega_dict[dev.name][interface] = {}
                    mega_dict[dev.name][interface]["status"] = output["interface"][interface]["status"]
                    mega_dict[dev.name][interface]["protocol"] = output["interface"][interface]["protocol"]
                    smaller_tabular = []
                    smaller_tabular.append(dev.name)
                    smaller_tabular.append(interface)
                    smaller_tabular.append(output["interface"][interface]["status"])
                    smaller_tabular.append(output["interface"][interface]["protocol"])
                    #review if condition to adjust to desired result
                    if output["interface"][interface]["status"] == "administratively down":
                        smaller_tabular.append('Passed')
                    elif ((output["interface"][interface]["status"] == "up" or 
                        output["interface"][interface]["protocol"] == "down") and
                        (output["interface"][interface]["status"] == "down")):
                        smaller_tabular.append('Failed')
                    else:
                        smaller_tabular.append('Passed')
                    mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['Interface', 'Status',
                                   'Protocol', 'Passed/Failed'],
                          tablefmt='orgtbl'))
        #review if condition to adjust to desired result
        for dev_name in mega_dict:
            for interface in mega_dict[dev_name]:
                if ((mega_dict[dev_name][interface]["status"] == "up" or 
                    mega_dict[dev_name][interface]["protocol"] == "down") and
                    (mega_dict[dev_name][interface]["status"] == "down")):
                    self.failed("{d}: {int} is in a not ok state, Status: {s} Protocol: {p}".format(
                        d=dev_name, int=interface, s=mega_dict[dev_name][interface]["status"], p=mega_dict[dev_name][interface]["protocol"]))
        self.passed("All interfaces are up or administratively down")


    @ aetest.test
    def check_ip_protocols(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = []
                log.info(banner("Gathering IP Protocol Information from {}".format(
                    dev.name)))
                output = dev.parse('sh ip protocols')
                smaller_tabular = []
                smaller_tabular.append(dev.name)
                gateways = output["protocols"]["isis"]["vrf"]["default"]["address_family"]["ipv4"]["instance"]["CUSTOMER_NAME"]["routing_information_sources"]["gateway"].keys()
                mega_dict[dev.name] = gateways
                smaller_tabular.append(", ".join(gateways))
                if set(gateways).issubset(set(test_params.params["routers_addr"])):
                    smaller_tabular.append('Passed')
                else:
                    smaller_tabular.append('Failed')
                mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['ISIS Gateways',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        for dev_name in mega_dict:
            if not set(mega_dict[dev_name]).issubset(set(test_params.params["routers_addr"])):
                self.failed("{d}: Does not contain all the routers, it contains: {e}".format(
                        d=dev_name, e=", ".join(mega_dict[dev_name])))
        self.passed("All devices' slots are in a ok state")
                

    @ aetest.test
    def check_isis_neighbors(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = 0
                log.info(banner("Gathering Isis Neighbors Information from {}".format(
                    dev.name)))
                output = dev.parse('sh isis neighbors') 
                nNeighbors = len(output["isis"]["CUSTOMER_NAME"]["neighbors"])
                mega_dict[dev.name] = nNeighbors
                smaller_tabular = []
                smaller_tabular.append(dev.name)
                smaller_tabular.append(", ".join(output["isis"]["CUSTOMER_NAME"]["neighbors"]))
                smaller_tabular.append(nNeighbors)
                if nNeighbors == test_params.params["nIsisNeighbors"]:
                    smaller_tabular.append('Passed')
                else:
                    smaller_tabular.append('Failed')
                mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['Neighbors', 'Number of Neighbors',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))
        for dev_name in mega_dict:
            if mega_dict[dev_name] != test_params.params["nIsisNeighbors"]:
                self.failed("{d}: has {e} isis neighbors, instead of 2".format(
                    d=dev_name, e=mega_dict[dev_name]))
        self.passed("All devices have 2 isis neighbors")

    @ aetest.test
    def check_ip_routes(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering IP Routes Information from {}".format(
                    dev.name)))
                output = dev.parse('show ip route')
        # Not sure what to review to decide if test is passing or failed
        self.failed("Failed? Fail or Passing criteria not specified")
                
                
# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################


# This is how to create a CommonCleanup
# You can have 0 , or 1 CommonCleanup.
# CommonCleanup can be named whatever you want :)
class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    # CommonCleanup follow exactly the same rule as CommonSetup regarding
    # subsection
    # You can have 1 to as many subsections as wanted
    # here is an example of 1 subsection

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")


if __name__ == '__main__':  # pragma: no cover
    aetest.main()
