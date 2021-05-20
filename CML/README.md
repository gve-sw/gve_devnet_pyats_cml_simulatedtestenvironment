# How to set-up a lab in CML

After having successfully installed CML, we can set-up a lab in CML. In order to
have a consistent and reproducible lab, we recommend an automated set-up with the `create_cml.py` python script. 

Before we can use that script, we have to make sure that the environment variables
have been added to the config file. 

    config = {}

    config['CML_SERVER_URL'] = "<REPLACE WITH YOUR THE URL OF THE CML SERVER>"
    config['CML_USERNAME'] = "<REPLACE WITH THE CML USERNAME>"
    config['CML_PASSWORD'] = "<REPLACE WITH THE CML PASSWORD>"
    config['LAB_NAME'] = "<REPLACE WITH THE LAB NAME>"
    config['IMAGE_DEFINITION'] = "<REPLACE WITH THE IMAGE DEFINITION>" 
    
    config['WEBEX_TOKEN'] = "<REPLACE WITH YOUR WEBEX TOKEN>"
    config['roomId'] = "<REPLACE WITH YOUR WEBEX ROOM ID>"

For `create_cml.py`, only the variables `'CML_SERVER_URL'`, `'CML_USERNAME'`,  `'CML_PASSWORD'`, `'LAB_NAME'`, and `'IMAGE_DEFINITION'` are needed. The latter two 
variables are for notification purposes. All of these
variables are strings. Moreover, we need to add the config files to the config subdirectory. 
The config files are all plaintext files. 
The names of the config files will also be the name of the devices, e.g., 
a config file with the name `"MBO-SPL-TST-010.txt"` will result in a device with the name
`MBO-SPL-TST-010`. 

In order to run the script, we have to run the following commands:

    $ cd CML
    $ python create_cml.py

The script will establish a connection with the CML server and then create a new lab with
the name provided in the config file as `LAB_NAME`. The lab will create the topology and use
the image definition provided in the `IMAGE_DEFINITION` variable (string). For this
proof of value, we had two options: `"CSR1000v-16.2.2"` and `"csr1000v-170301a"`. However, you can 
upload your own image definition as desired. Then, the configuration files are read in and
we also obtain a testbed file in yaml format. This file will be used for pyATS in the next step. 

## Screen recording of automated set-up of CML
Below, you will find a screen recording of the automated set-up of CML. You will have side-by-side view 
of the CML GUI and the terminal. You will see the changes that are applied through the API right away 
in the GUI.

![CML_automated](./IMAGES/cml_automated_setup.gif)

## Infographic of the process

![CML_infographic](./IMAGES/cml_infographic.png)

## Limitations
Limitations that were encountered during the project:
- **Caution**: CML v2.x does not operate with full functionality on Mac OS Big Sur as of May 2021.
- **Caution**: Due to CML's limitations, BFD is not supported. 
- ASR routers are not supported in CML, but we opted for CSR1000v instead, which also runs IOS-XE
- All the configuration and show commands related to hardware are not supported in CML


## How to use the GUI of CML
In order to use the GUI of CML, we go the URL of the server where CML is hosted. We can log in with our username and password. See below for an example. 

![CML_login](./IMAGES/cml_log_in.png)

After having successfully logged in, we will see the dashboard of CML. Please note that your dashboard might look slightly different, depending on the version that you are using. 
From this view, we can easily start, stop, wipe or delete a node. Moreover, we can also easily import a lab or search for an exisiting lab. In the tools menu, 
we can add additional image definitions and configure your personal account. 

![CML_dashboard](./IMAGES/cml_dashboard.png)

You can easily start a new lab and all of these labs are independent of each other. Moreover, you can easily collaborate on one server without affecting the other users. 
When we click on one of the labs, we enter the workbench view. We get an overview of the topology and we can click on the nodes and links, which will give us options to configure them. 


![CML_lab](./IMAGES/cml_lab.png)

In the bottom menu, we have several submenus that gives us more granular info about the nodes. 
In this case, we see the connectivity between the nodes and interfaces. 

![CML_connectivity](./IMAGES/cml_connectivity.png)

Moreover, we can also configure the number of interfaces. We can easily add additional interfaces if needed.
![CML_interfaces](./IMAGES/cml_interfaces.png)












