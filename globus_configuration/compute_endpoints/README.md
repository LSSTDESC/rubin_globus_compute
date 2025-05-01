# Globus Compute Endpoint Configuration

This folder provides instructions on how to configure and deploy Globus Compute endpoints on the HPC cluster. The endpoint is reponsible to interface with the local scheduler and execute tasks (Globus functions) remotely on the compute nodes.

**Note**: Every command below should be executed within your python virtual environment (see README in the previous `globus_configuration` folder).

## Endpoint Initialization

Name your compute endpoint:
```bash
# Here "inside" refers to the Globus worker being deployed within the container directly
ENDPOINT_NAME="rubin_inside_container_endpoint"
```

Initialize your endpoint:
```bash
globus-compute-endpoint configure ${ENDPOINT_NAME}
```

Replace the content of the `config.yaml` (located at `~/.globus_compute/${ENDPOINT_NAME}/config.yaml`) with the content of one of the YAML files found in this folder. Make sure to customize the `PLACEHOLDER`s to adapt the configuration to your work environment. 

Start and deploy the endpoint (this might trigger a Globus authentication flow):
```bash
globus-compute-endpoint start ${ENDPOINT_NAME}
```

## Endpoint Management

Check if your endpoint is running and recover its UUID:
```bash
globus-compute-endpoint list
```

If you change the configuration file, you need to restart the endpoint:
```bash
globus-compute-endpoint restart ${ENDPOINT_NAME}
```

You can stop the entpoint with:
```bash
globus-compute-endpoint stop ${ENDPOINT_NAME}
```