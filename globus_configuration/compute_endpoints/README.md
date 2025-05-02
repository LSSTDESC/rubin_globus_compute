# Globus Compute Endpoint Configuration

This folder provides instructions on how to configure and deploy the Globus Compute endpoint on the HPC cluster. The endpoint is reponsible to interface with the local scheduler and execute tasks (Globus functions) within containers running on compute nodes. The task execution (see the `compute_functions` folder) can all be done remotely. 

**Prerequisites**: The following instructions assume that you already have an Apptainer `.sif` or `.sing` file ready.

**Note**: Every command below should be executed within your python virtual environment (see README in the previous `globus_configuration` folder).

## Initialize Your Endpoint

Create a Globus Compute endpoint on the HPC cluster:
```bash
ENDPOINT_NAME="lsst_desc_endpoint"
globus-compute-endpoint configure ${ENDPOINT_NAME}
```

Replace the content of the endpoint configuration file (located on the HPC cluster at `~/.globus_compute/${ENDPOINT_NAME}/config.yaml`) with the content of the `polaris_config.yaml` file located in this folder. Make sure to customize the `PLACEHOLDER` to include the path to your `.sif` or `.sing` Apptainer file.

Start and deploy the endpoint (this might trigger a Globus authentication flow):
```bash
globus-compute-endpoint start ${ENDPOINT_NAME}
```

## Manage Your Endpoint

Check if your endpoint is running (also useful to recover its UUID):
```bash
globus-compute-endpoint list
```

If you change the configuration file, you need to restart the endpoint:
```bash
globus-compute-endpoint restart ${ENDPOINT_NAME}
```

Stop the endpoint (bring offline):
```bash
globus-compute-endpoint stop ${ENDPOINT_NAME}
```

Delete the endpoint (complete removal from the system):
```bash
globus-compute-endpoint delete ${ENDPOINT_NAME}
```