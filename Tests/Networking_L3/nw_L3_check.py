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

class nw_L3(aetest.Testcase):
    """ This is user Testcases section """

    @ aetest.test
    def check_mpls_ldp_neighbor(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering MPLS LDP Neighbor Information from {}".format(
                    dev.name)))
                output = dev.parse('show mpls ldp neighbor')
                for peer in output["vrf"]["default"]["peers"]:
                    smaller_tabular = []
                    smaller_tabular.append(dev.name)
                    smaller_tabular.append(peer)
                    state = output["vrf"]["default"]["peers"][peer]["label_space_id"][0]["state"]
                    smaller_tabular.append(state)
                    mega_dict[dev.name][peer] = state
                    if state == "oper":
                        smaller_tabular.append('Passed')
                    else:
                        smaller_tabular.append('Failed')
                    mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['Peer', 'State',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))
        for dev_name in mega_dict:
            for peer in mega_dict[dev_name]:
                if mega_dict[dev_name][peer] != "oper":
                    self.failed("{d}: {p} is in a not in a oper state: {e}".format(
                        d=dev_name, p=peer, e=ega_dict[dev_name][peer]))
        self.passed("All mpls neighbors are in oper state")
                

    @ aetest.test
    def check_mpls_ldp_bindings(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering MPLS LDP Bindings Information from {}".format(
                    dev.name)))
                output = dev.parse('show mpls ldp bindings')
        #No idea on how to check MPLS bindings for each device is correct
        self.failed("Failed?")
    
    @ aetest.test
    def check_mpls_fw_table(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering MPLS Forwarding Table Information from {}".format(
                    dev.name)))
                output = dev.parse('show mpls forwarding-table')
        #No idea on how to check Ensure labels are assigned for all required prefixes
        self.failed("Failed?") 
                
                
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
