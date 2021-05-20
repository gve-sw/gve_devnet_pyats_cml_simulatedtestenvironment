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

#Env variables
cml_server_url = env.config['CML_SERVER_URL']
cml_username = env.config['CML_USERNAME']
cml_password = env.config['CML_PASSWORD']

#connect
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = ClientLibrary(cml_server_url, cml_username, cml_password, ssl_verify=False, raise_for_auth_failure=True, allow_http=True)

#get lab
lab = client.find_labs_by_title("Jupyter Lab")[0]

#get lab testbed
pyats_testbed = lab.get_pyats_testbed()

#Add credentials to yaml file
doc = yaml.load(pyats_testbed)
doc["devices"]["terminal_server"]["connections"]["cli"]["username"] = cml_username
doc["devices"]["terminal_server"]["connections"]["cli"]["password"] = cml_password

# Write the YAML testbed out to a file
with open("lab_testbed.yaml", "w") as f: 
    yaml.dump(doc,f)

#run command in a node
lab = client.join_existing_lab(lab.id)
print("Device -> "+str(lab.nodes()[0]))
node = lab.get_node_by_id(lab.nodes()[0].id)
lab.pyats.sync_testbed(cml_username, cml_password)
version = node.run_pyats_command("show config")
print(version)

