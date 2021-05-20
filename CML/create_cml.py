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
import logging
import os, sys
# env is in parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import env

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

# Read environment variables
cml_server_url = env.config['CML_SERVER_URL']
cml_username = env.config['CML_USERNAME']
cml_password = env.config['CML_PASSWORD']
LAB_TITLE = env.config['LAB_NAME']
IMAGE_DEFINITION = env.config['IMAGE_DEFINITION']
log.info("LOGGING INFO: Successfully read in the environment variables")

# Connect with the CML API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = ClientLibrary(cml_server_url, cml_username, cml_password, ssl_verify=False, raise_for_auth_failure=True, allow_http=True)
log.info("LOGGING INFO: Successfully connected with CML through the API")

# Read in the config file
config_files = os.listdir(path='./config')
config_files = [file for file in config_files if ".txt" in file]
log.info("LOGGING INFO: Successfully read in the config files")

routers = []
for file in config_files:
    routers.append(file[:-4])

# Create a new lab in CML
lab = client.create_lab(title=LAB_TITLE)
log.info("LOGGING INFO: Successfully created the lab in CML")

# Create the nodes in the lab
coordinates = [(0,0), (200, 0), (200,200), (0, 200)]
coordinates_counter = 0 
for router in routers:
    x, y = coordinates[coordinates_counter]
    lab.create_node(label=router, node_definition='csr1000v', populate_interfaces=8, x=x, y=y)
    coordinates_counter += 1
log.info("LOGGING INFO: Successfully created the nodes in the lab")
    
# Configure the nodes in the lab
for node in lab.nodes():
    config = open(f"./config/{node.label}.txt", 'r').read()
    node.config = config
    node.image_definition = IMAGE_DEFINITION
log.info("LOGGING INFO: Successfully configured the nodes in the lab")

# Connect the nodes to each other
interface_pairs = [('010', '020'), ('020', '030'), ('030', '040'), ('040', '010')]
for intf1, intf2 in interface_pairs:
    for interface in lab.interfaces():
        if intf1 in interface.node.label and '2' in interface.label:
            interface1 = interface
        if intf2 in interface.node.label and '3' in interface.label:
            interface2 = interface
    lab.create_link(interface1, interface2)
log.info("LOGGING INFO: Successfully created links between the nodes")

#get lab testbed
pyats_testbed = lab.get_pyats_testbed()
# Write the YAML testbed out to a file
with open("lab_testbed.yaml", "w") as f: 
    f.write(pyats_testbed)
log.info("LOGGING INFO: Successfully obtained a testbed file")