# Overview

This check connects to all devices defined in the testbed, and parses device
commands for checking its health. The checked commands are the following:
* **show mpls ldp neighbor:** Verify all required MPLS sessions are setup, checks if they are in oper state.
* **show mpls ldp bindings:** Verify the MPLS bindings for each device is correct. Passing/failed condition not implemented as not sure how to check the condition from the output.
* **show mpls forwarding-table:** Verify tlabels are assigned for all required prefixes. Passing/failed condition not implemented as not sure how to check the condition from the output.
# Running

```
easypy nw_L3_check_job.py -html_logs -testbed_file <path_to_testbed>
```

## How to send webex alert

Leveraging some of the PyATS pluggings, we can easily send a webex alert after a test is done and we can send a short summary through a bot. If there is no space specified, then it will be sent to the user. 

In case you want to send it to a user:

    pyats run job <COMMANDS_JOB>.py --testbed-file <testbed_file>.yaml --webex-token <WEBEX_BOT_TOKEN> --webex-email <MY_EMAIL> 
    
In case you want to send it to a space:

    pyats run job <COMMANDS_JOB>.py --testbed-file <testbed_file>.yaml --webex-token <WEBEX_BOT_TOKEN> --webex-space <MY_SPACE_ID>