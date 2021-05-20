# Running commands using PyATS

This repository contains 2 scripts to show basic cases of operations ran using pyATS. This scripts have been tested using a simulated network on CML, but in case that wants to be applied to another simulated or real test environment, the user should alter the lab_testbed.yaml, as it is used t connect with the different devices and interact with them.

![Drag Racing](/IMAGES/testbed.png)

## Environment

For setting up the environment remember to have a testbed of your simulated or real environment and create a env.py file with the following variable definitions, as will be used to interact with the lab and its devices
```Python
config = {}

config['CML_SERVER_URL'] = "<REPLACE WITH YOUR THE URL OF THE CML SERVER>"
config['CML_USERNAME'] = "<REPLACE WITH THE CML USERNAME>"
config['CML_PASSWORD'] = "<REPLACE WITH THE CML PASSWORD>"
config['WEBEX_TOKEN'] = "<REPLACE WITH YOUR WEBEX TOKEN>"
config['roomId'] = "<REPLACE WITH YOUR WEBEX ROOM ID>"
```

## Get config 

The get-config-virlpyats.py script is a simple example for running remote commands in network devices and collecting the output. The general flow of this script is first to connect with the CML lab instance with the according credentials and parameters, then obtain the lab information and testbed, afterwards connects to a specific network device to run a "show config" command and print the output.

![use cases commands](/IMAGES/running_commands.png)

It serves as a very simple and straight to the point proof of concept on how to connect to a CML lab and its devices and then run operations in them.

## Diff

Diff operations have the purpose of checking the state of a same subject at 2 different points in time and be able to extract the differences between them. In the industry they are very useful as allow to extract very valuable information and insight, and as a result they are part of many recurrent development tools like git.

![diff](/IMAGES/diff.png)

For the standpoint of a network administrator it can be incredibly time saving and effective when identifying and tracking network changes, for troubleshooting, documenting or running tests. In a nutshell, the developed script config_diff_pyats.py leverages the learn functionality of pyATS in order to capture a snapshot of the device configuration, then applies a change in the network, take another snapshot and finally compares the two versions, extracting the differences in between them.

![Learn](/IMAGES/learn.png)

The [learn functionality](https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/learndevices.html#) is extremely valuable to gather the current state of the network, basically it has predefined commands to gather information from the devices based on specific tags, like "all", "acl" or "ospf", between a lot more. When executing the simple function runs all the specific commands and gathers this information in a dictionary for further usage.

![Use case diff](/IMAGES/diff_use_case.png)

In the case of the developed script, the snapshots are a complete image of the device configuration, as uses "all" as parameter for the learn pyATS library. After that stores it in a json file under learn_results/, then applies the necessary commands to create a new Loopback interface with a random interface number, then repeats the process and learns all features of the devices and finally generates a diff file under diff_results/ . This process is repeated on all devices as loops through a collection of them taken from the lab testbed.
