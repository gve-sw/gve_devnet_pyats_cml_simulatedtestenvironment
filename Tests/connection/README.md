# Overview

This check connects to all devices defined in the testbed, and parses device
commands for checking its health. The checked commands are the following:
* **show platform:** Verify if all modules installed are state is OK.
* **show version:** Verify if the version specified in test_params.py is the operating one in all the devices. This test case has an issue parsing the command, should be fixed in a future version of PyATS.
* **show processes cpu history:** Verify the CPU utilization if the CPU is above a threshold specified in test_params.py.
* **show redundancy:** Verify that both RSP’s are active and the mode is SSO 

# Running

```
easypy connection_example_job.py -html_logs -testbed_file <path_to_testbed>
```


## How to send webex alert

Leveraging some of the PyATS pluggings, we can easily send a webex alert after a test is done and we can send a short summary through a bot. If there is no space specified, then it will be sent to the user. 

In case you want to send it to a user:

    pyats run job <COMMANDS_JOB>.py --testbed-file <testbed_file>.yaml --webex-token <WEBEX_BOT_TOKEN> --webex-email <MY_EMAIL> 
    
In case you want to send it to a space:

    pyats run job <COMMANDS_JOB>.py --testbed-file <testbed_file>.yaml --webex-token <WEBEX_BOT_TOKEN> --webex-space <MY_SPACE_ID>