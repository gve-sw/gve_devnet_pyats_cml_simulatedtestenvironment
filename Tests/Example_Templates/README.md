# Example Templates
This two folders contain more deeply and simplified examples to understand the test flow easily. 

## File Structure
Each of the folders contains 3 files that are relevant for the test execution:

* **test_file.py**: this file contains the different sections to be executed, incluiding a setup, test sections and a cleaning section. Each of them are defined following the indications from the [Aetest documentation](https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html), and as observed they are defined as clasess and subclasess with *@markers* for the further test execution. This file is where you should define the actions taken by your tests and depending on the information gathered if they are succesful or not.

* **test_file_job.py**: the job file is necesary as we will be running the test scripts with the help of easypy and it requires to use the run function included in a main function. Remember to define the correct path to the *test_file.py* file.

* **test_params.py**: for the purpose of scalability, modularity and avoid hardcoding variables, this file is where you should include variables relevant for the testcase that can be altered, as could be thresholds, specific tags or any variable that can be relevant to configure before executing the test cases


## Execution

The execution is done using [easypy](https://pubhub.devnetcloud.com/media/pyats/docs/easypy/introduction.html) which is a pyATS moduled designed for this purpose

## Examples

The examples actually implement the same test, which is checking for CRC errors in all the devices of the testbed and if any are found the test will count as a failure.

* **Simple Test:** it is the simplest of the two testcases, it just executes a command per device and looks for CRC errors in the result. Based on that considers if it has been a success or failure.

* **Console Summary Test:** builds an extra functionality on top of the simple test previously explained. As reading from CLI output can be quite tiring, this one also extracts the valuable information and represents it into a summary table before considering the passing or faling state of the test.

<img src="/IMAGES/console_summary_output.png">