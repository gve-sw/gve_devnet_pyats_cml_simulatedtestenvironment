# Overview

This check connects to all devices defined in the testbed, and parses device
commands for checking its health. The checked commands are the following:
* **show ip interface brief:** Verify if protocols and statuses of interfaces are correct state.
* **sh ip protocols:** Verify that all routers defined in test_params.py are visible in the ISIS output
* **sh isis neighbors:** Verify that each router has 2 ISIS neighbors
* **show ip route:** Verify that all routes are visible, not fully implemented as not sure about which routes should be included.

![use case L1L2](/IMAGES/use_case_L1L2.png)


# Running

```
easypy nw_L1_L2_check_job.py -html_logs -testbed_file <path_to_testbed>
```

## How to send webex alert

Leveraging some of the PyATS pluggings, we can easily send a webex alert after a test is done and we can send a short summary through a bot. If there is no space specified, then it will be sent to the user. 

In case you want to send it to a user:

    pyats run job <COMMANDS_JOB>.py --testbed-file <testbed_file>.yaml --webex-token <WEBEX_BOT_TOKEN> --webex-email <MY_EMAIL> 
    
In case you want to send it to a space:

    pyats run job <COMMANDS_JOB>.py --testbed-file <testbed_file>.yaml --webex-token <WEBEX_BOT_TOKEN> --webex-space <MY_SPACE_ID>