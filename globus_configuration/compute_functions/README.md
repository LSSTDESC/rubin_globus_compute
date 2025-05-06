# Globus Compute Function Registration

This folder provides instructions on how to execute Globus Compute tasks that interact with containers running on compute nodes. Requests to execute Globus Compute functions will be sent to the Globus server, which will relay the request down to your Compute endpoint.

**Prerequisites**: The following instructions assume that you already have:
1. a Globus Compute endpoint deployed and running on Polaris,
2. an Apptainer `.sing` or `.sif` file accessible from the filesystem.

## Register Your Function

Register the test function by executing the python file:
```bash
python register_test_function.py
```
The above command should print the registered function UUID, which is also stored in the `uuid_test_function.txt` file for future reference. 

## Test Your Function

Create a `.env` environment file (in the current folder where this README file is) and add the following:
```bash
ENDPOINT_ID="PLACEHOLDER --> UUID of your deployed Globus Compute endpoint"
FUNCTION_ID="PLACEHOLDER --> UUID of your registered Globus Compute function"
SIF_SING_PATH="PLACEHOLDER --> /full/path/to/your/.sing_or_.sif_file"
```

Submit your Globus Compute task by executing the following script:
```bash
python run_function.py
```

If successful, this should return the python executable from the LSST environment:
```bash
gdfb3db0272+00fb23383b 	current w_2025_17 setup
/opt/lsst/software/stack/conda/envs/lsst-scipipe-10.0.0/bin/python
```
