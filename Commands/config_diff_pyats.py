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
from random import randrange
import sys
import time
import logging
import json
from genie.testbed import load
from pyats.log.utils import banner
from pyats.topology import loader
from genie.utils.diff import Diff
import yaml
import datetime 
import os
import requests


# Env variables
cml_server_url = env.config['CML_SERVER_URL']
cml_username = env.config['CML_USERNAME']
cml_password = env.config['CML_PASSWORD']
webex_token = env.config['WEBEX_TOKEN']
webex_roomId = env.config['roomId']

# Enable logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

# Saves Learn output info to a json file
def learn_to_file(learned, file_name):
    clean_output={}
    for item in output1:
        log.info(banner(item))
        if hasattr( output1[item] , "info" ):
            clean_output[item] = output1[item].info
        else:
            clean_output[item] = ""

    with open(file_name, "w") as f: 
        json.dump(clean_output, f, indent = 3)

# Creates a random loopback interface in a device
def loopback_change(device):
    device.configure(f'''
                    interface Loopback {randrange(700,1023)}
                    description New Interface Created with Genie change
                    ''')

# Alters a testbed file to place the needed credentials to connect to devices
def add_cml_credentials(testbed, filename, username, password):
    doc = yaml.load(testbed)
    doc["devices"]["terminal_server"]["connections"]["cli"]["username"] = cml_username
    doc["devices"]["terminal_server"]["connections"]["cli"]["password"] = cml_password
    # Write the YAML testbed out to a file
    with open(filename, "w") as f: 
        yaml.dump(doc,f)

# Send file to Webex Room
def sendFile(roomId, webex_token, file_name, path):
    url = "https://webexapis.com/v1/messages"
    payload={'roomId': roomId,
    'text': f'Report file: {file_name}'}
    files=[
    ('files',(file_name, open(path,'rb'), 'application/json'))
    ]
    headers = {
    'Authorization': f'Bearer {webex_token}',
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response.raise_for_status()


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = ClientLibrary(cml_server_url, cml_username, cml_password, ssl_verify=False, raise_for_auth_failure=True, allow_http=True)
    
    #get lab
    lab = client.find_labs_by_title("Jupyter Lab")[0]

    #get lab testbed
    pyats_testbed = lab.get_pyats_testbed()

    #add credentials to testbed
    add_cml_credentials(pyats_testbed, "lab_testbed.yaml", cml_username, cml_password)

    #create directories if doesn't exist
    if not os.path.exists("./learn_results"):
        os.makedirs("./learn_results")
    if not os.path.exists("./diff_results"):
        os.makedirs("./diff_results")
    
    #load testbed
    log.info(banner("Loading testbed"))
    testbed = loader.load('lab_testbed.yaml')
    log.info("\nPASS: Successfully loaded testbed '{}'\n".format(testbed.name))
    for device_name in testbed.devices:
        if device_name != "terminal_server":
            #connect
            log.info(banner(f"CONNECT {device_name}"))
            device = testbed.devices[device_name]
            device.connect()

            ## learn 1
            log.info(banner("LEARN"))
            output1 = device.learn('all')
            learn_to_file( output1, f"learn_results/{device}learn_result1.json")

            ## apply change
            log.info(banner("CHANGE"))
            loopback_change(device)

            ## learn 2
            log.info(banner("LEARN2"))
            output2 = device.learn('all')
            learn_to_file( output2, f"learn_results/{device}-learn_result2.json")

            ## diff
            log.info(banner("DIFF"))
            total_diff = ""
            for item in output1:
                log.info("DIFF "+str(item))
                if hasattr( output1[item] , "info" ) and hasattr( output2[item] , "info" ):
                    loopback_diff = Diff(output1[item].info, output2[item].info)
                    loopback_diff.findDiff()
                    if str(loopback_diff) != "":
                        log.info(str(loopback_diff))
                        total_diff += (f"""DIFF {str(item)}\n"""
                                    f"""{str(loopback_diff)}\n\n""")
            ## diff to file
            filename = f"diff-{device}-{str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))}.diff"
            with open(f"./diff_results/{filename}", "w") as f: 
                f.write(total_diff)
    #Reporting in Webex
    diff_results = os.listdir("./diff_results")
    for file in diff_results:
        sendFile(webex_roomId, webex_token, file, f"./diff_results/{file}")





