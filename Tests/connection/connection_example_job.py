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
import os
from pyats.easypy import run

# To run the job:
# pyats run job $VIRTUAL_ENV/examples/connection/job/connection_example_job.py \
#               --testbed-file <your tb file>
#
# Description: This example uses a sample testbed, connects to a device
#              which name is passed from the job file,
#              and executes some commands.

# All run() must be inside a main function
def main():
    # Find the location of the script in relation to the job file
    test_path = os.path.dirname(os.path.abspath(__file__))
    testscript = os.path.join(test_path, 'connection_example_script.py')

    # Execute the testscript
    run(testscript=testscript)
