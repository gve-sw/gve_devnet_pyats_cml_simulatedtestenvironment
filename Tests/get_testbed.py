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

import urllib3
from virl2_client import ClientLibrary
from virl2_client.models.cl_pyats import ClPyats
import yaml
import os
import env
from genie.utils.diff import Diff
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

#Script for gathering testbed from CML

#Environment variables
cml_server_url = env.config['CML_SERVER_URL']
cml_username = env.config['CML_USERNAME']
cml_password = env.config['CML_PASSWORD']

#connect
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = ClientLibrary(cml_server_url, cml_username, cml_password, ssl_verify=False, raise_for_auth_failure=True, allow_http=True)

#setup config files
config_files = os.listdir(path='./config')
config_files = [file for file in config_files if ".txt" in file]

#get lab
lab = client.find_labs_by_title("BRAIN 16.2")[0]
print(lab)

#get lab testbed
pyats_testbed = lab.get_pyats_testbed()
# Write the YAML testbed out to a file
with open("lab_testbed.yaml", "w") as f: 
    f.write(pyats_testbed)