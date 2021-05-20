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

class verify_platform(aetest.Testcase):
    """ This is user Testcases section """

    @ aetest.test
    def check_slot_state(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering Platform Information from {}".format(
                    dev.name)))
                output = dev.parse('show platform')
                for slot in output["slot"]:
                    mega_dict[dev.name][slot] = {}
                    for type in output["slot"][slot]:
                        state = output["slot"][slot][type]["CSR1000V"]["state"]
                        mega_dict[dev.name][slot]["state"] = state
                        smaller_tabular = []
                        smaller_tabular.append(dev.name)
                        smaller_tabular.append(output["slot"][slot][type]["CSR1000V"]["slot"])
                        smaller_tabular.append(state)
                        if "ok" in state:
                            smaller_tabular.append('Passed')
                        else:
                            smaller_tabular.append('Failed')
                        mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['Slot', 'State',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        for dev_name in mega_dict:
            for slot in mega_dict[dev_name]:
                if not ("ok" in mega_dict[dev_name][slot]["state"]):
                    self.failed("{d}: {slot} is in a not ok state: {e}".format(
                        d=dev_name, slot=slot, e=mega_dict[dev_name][slot][state]))
        self.passed("All devices' slots are in a ok state")


class verify_version(aetest.Testcase):
    """ This is user Testcases section """

    # License checking to be implemented

    @ aetest.test
    def check_version(self):
        '''
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering Software Version Information from {}".format(
                    dev.name)))
                output = dev.parse('show version')
                mega_dict[dev.name] = output["version"]["version"]
                smaller_tabular = []
                smaller_tabular.append(dev.name)
                smaller_tabular.append(output["version"]["version"])
                if output["version"]["version"] == test_params.params["sw_version"]:
                    smaller_tabular.append('Passed')
                else:
                    smaller_tabular.append('Failed')
                mega_tabular.append(smaller_tabular) 
        log.info(tabulate(mega_tabular,
                          headers = ['SW Version', 'Passed/Failed'],
                          tablefmt='orgtbl'))
        
        for dev_name in mega_dict:
            if mega_dict[dev_name] != test_params.params["sw_version"]:
                self.failed("{d}: version is {e} instead of {version}".format(
                    d=dev_name, e=mega_dict[dev_name], version=test_params.params["sw_version"]))
        self.passed("All devices have the correct software version: {version}".format(
                    version=test_params.params["sw_version"]))
        '''
        # There is an error parsing the output of the show version command, will probably be fixed
        # in a future update of the pyATS/Genie Library
        self.failed("""
            Failed?, There is an error parsing the output of the show version command, will probably be fixed
            in a future update of the pyATS/Genie Library
            """)



class verify_processes_cpu(aetest.Testcase):
    """ This is user Testcases section """

    @ aetest.test
    def check_process_cpu(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering CPU Usage Information from {}".format(
                    dev.name)))
                output = dev.parse('show processes cpu history')
                for time_frame in output:
                    max = 0
                    max_avg = 0
                    mega_dict[dev.name][time_frame] = {}
                    mega_dict[dev.name][time_frame]["maximum"] = []
                    mega_dict[dev.name][time_frame]["average"] = []
                    for sample in output[time_frame]:
                        mega_dict[dev.name][time_frame]["average"].append(output[time_frame][sample]["average"])
                        mega_dict[dev.name][time_frame]["maximum"].append(output[time_frame][sample]["maximum"])
                        if output[time_frame][sample]["maximum"] > max:
                            max = output[time_frame][sample]["maximum"]
                        if output[time_frame][sample]["average"] > max_avg:
                            max_avg = output[time_frame][sample]["average"]
                    smaller_tabular = []
                    smaller_tabular.append(dev.name)
                    smaller_tabular.append(time_frame)
                    smaller_tabular.append(max)
                    smaller_tabular.append(max_avg)
                    if max_avg < test_params.params["max_cpu"] or max < test_params.params["max_cpu"]:
                        smaller_tabular.append('Passed')
                    else:
                        smaller_tabular.append('Failed')
                    mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['Time Span', 'Max', 'Max Avg',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        for dev_name in mega_dict:
            for time_frame in mega_dict[dev_name]:
                for sample in mega_dict[dev.name][time_frame]["maximum"]:
                    if sample > test_params.params["max_cpu"]:
                        self.failed("{d}: in timespan {ts} a sample was over {value} cpu usage".format(
                            d=dev_name, ts=time_frame, value=sample))
        
        self.passed("All recorded values for CPU usage in all devices where lower than {value}". format(value=test_params.params["max_cpu"]))


class verify_redundancy(aetest.Testcase):
    """ This is user Testcases section """

    @ aetest.test
    def check_redundancy(self):
        mega_dict = {}
        mega_tabular = []
        for dev in self.parent.parameters['dev']:
            if dev.name == "terminal_server":
                pass
            else:
                mega_dict[dev.name] = {}
                log.info(banner("Gathering Redundancy Information from {}".format(
                    dev.name)))
                output = dev.parse('show redundancy')
                mega_dict[dev.name]["conf_red_mode"] = output["red_sys_info"]["conf_red_mode"]
                mega_dict[dev.name]["oper_red_mode"] = output["red_sys_info"]["oper_red_mode"]
                ############################################
                ###Implement STANDBY HOT check in the future
                ############################################
                smaller_tabular = []
                smaller_tabular.append(dev.name)
                smaller_tabular.append(output["red_sys_info"]["conf_red_mode"])
                smaller_tabular.append(output["red_sys_info"]["oper_red_mode"])
                if output["red_sys_info"]["conf_red_mode"] == "sso" and output["red_sys_info"]["oper_red_mode"] == "sso":
                    smaller_tabular.append('Passed')
                else:
                    smaller_tabular.append('Failed')
                mega_tabular.append(smaller_tabular)
        log.info(tabulate(mega_tabular,
                          headers = ['Device', 'Configured Redundancy Mode', 'Operating Redundancy Mode',
                                   'Passed/Failed'],
                          tablefmt='orgtbl'))

        for dev_name in mega_dict:
            if mega_dict[dev_name]["conf_red_mode"] != "sso" or mega_dict[dev_name]["oper_red_mode"] != "sso":
                self.failed("{d}: Configured Redundancy Mode is {conf} and Operating Redundancy Mode is {oper}, instead of SSO".format(
                            d=dev_name, conf=mega_dict[dev_name]["conf_red_mode"], oper=mega_dict[dev_name]["oper_red_mode"]))

        self.passed("All recorded values for CPU usage in all devices where lower than {value}". format(value=test_params.params["max_cpu"]))


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
