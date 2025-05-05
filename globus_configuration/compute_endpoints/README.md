# Globus Compute Endpoint Configuration

This folder provides instructions on how to configure and deploy the Globus Compute endpoint on Polaris at ALCF. The endpoint is reponsible to interface with the local scheduler (PBS) and execute tasks (Globus functions) within containers running on compute nodes.

## Initialize Your Endpoint

On a login node, initialize the Globus Compute endpoint:
```bash
ENDPOINT_NAME="lsst_desc_endpoint"
globus-compute-endpoint configure ${ENDPOINT_NAME}
```

Replace the content of the endpoint configuration file (located on the HPC cluster at `~/.globus_compute/${ENDPOINT_NAME}/config.yaml`) with the content of the `polaris_config.yaml` file located in this folder. **Important**: Make sure the last line of the `worker_init` represents how your Globus Compute virtual environment is activated.

Start and deploy the endpoint (this might trigger a Globus authentication flow):
```bash
globus-compute-endpoint start ${ENDPOINT_NAME}
```

## Manage Your Endpoint

Check if your endpoint is running (also useful to recover its UUID):
```bash
globus-compute-endpoint list
```

If you modify the configuration file, you need to restart the endpoint:
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