# Globus Compute Function Registration

This folder provides instructions on how to execute commands within the containers using Globus Compute. Requests to execute Globus Compute functions will be sent to the Globus server, which will relay the request down to your Compute endpoint. 

**Prerequisites**: The following instructions assume that you already have a Globus Compute endpoint deployed and running on the HPC cluster.

**Note**: Every command below should be executed within your python virtual environment (see README in the previous `globus_configuration` folder).

## Register Your Function

Register the test function by executing the python file:
```bash
python register_test_function.py
```
The above command should print the registered function UUID, which is also stored in the `uuid_test_inside_function.txt` file for future reference. 

## Test Your Function

Create a `.env` environment file and add the following:
```bash
FUNCTION_ID="<PLACEHOLDER --> UUID of your registered Globus Compute function>"
ENDPOINT_ID="<PLACEHOLDER --> UUID of your deployed Globus Compute endpoint>"
```

Submit your Globus Compute task by executing the following script:
```bash
python run_function.py
```

If successful, this should return the output of the commands ran within the running container. In particular, the last command (`command -v python`) should return the executable from the LSST environment(`/opt/lsst/software/stack/conda/envs/lsst-scipipe-10.0.0/bin/python`).