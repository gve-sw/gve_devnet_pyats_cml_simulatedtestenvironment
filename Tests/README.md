# PyATS automatic testing

![NetDevops](/IMAGES/test_devops.png)

In this directory you will be able to find example scripts for automatic network testing by leveraging [PyATS](https://developer.cisco.com/docs/pyats/). The network being tested has been simulated using CML and the tested that refers to is lab_testbed.yaml, which was gathered using the get_testbed.py. For running in a different real or simulated environment, pay special care to to the testbed definition of it, as it is a key element for interacting with the network.

![NetDevops](/IMAGES/testing_flow.png)

The purpose of this use cases is assuring network reliability in an automatic and agile way for the network administrators. In a nutshell, each case runs different commands on all the specified devices in the network to collect data, after that aggregates it and then elaborates a passing or failing result statement for each case. Finally the result information is represented in different ways that summarize the result, actions taken and allows for a debugging of them.

Each of the subdirectories seen covers a different case, if looking for a deeply documented examples for learning and testing for the first time, it is recommended to go first on the Example_Tests directory, as it has been specifically designed for it. The rest of the directories are more deep and complete test cases for checking different conditions in the network anc can be used directly or serve as a good starting point for an already experienced network administrator on pyATS.

If looking for a deeper explanation of each case, there is a README.md file in each of the subdirectories specifying how to run the them and the general functionality, along with in code documentation.

This examples serve as proof of concept of some of the pyATS capabilities, but there is a lot more personalization and options that can be implemented, for that reason it is recommended to check the [official documentation](https://developer.cisco.com/docs/pyats/api/) for further enhancement.

# Requirements
* Python v3.6.x, v3.7.x and v3.8.x
* Tested platforms:
    * Linux (tested with CentOS, RHEL, Ubuntu, Alpine)
    * Mac OSX (10.13+)
* PyATS[full]


# Next Steps - Xpresso
[Xpresso](https://github.com/CiscoTestAutomation/xpresso) is the standard PyATS UI dashboard to streamline the network automation, test and validation experience.
Some of the high-level functionalities are
* Creating Job and Job Schedules
* Testbed Queueing
* Compare Job Test results
* Verification testing of software updates from Cisco
* Set baseline for job test results
* History tracking 
* Supports independent modules, webhook plugins, pluggables apps and more


Read [here](https://xpresso-sjc-1.cisco.com/documentation/assets/docs/getting_started/ui_feature/menubar.md) for a breakdown of major dashboard GUI elements.
Read [here](https://xpresso-sjc-1.cisco.com/documentation/assets/docs/quick_start.md) for a high-level to explore the most common and most used tasks, features and how to get started. 
