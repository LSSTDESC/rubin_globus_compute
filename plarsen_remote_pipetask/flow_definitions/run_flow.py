from globus_sdk import SpecificFlowClient, UserApp
from dotenv import load_dotenv
import os

# Public Globus thick client for authentication
AUTH_CLIENT_ID = "f818e8c5-61ba-4f70-8237-a8e69f266ae7"

# Load UUIDs
load_dotenv()

"""
Your .env file needs a number of items 

USERNAME="XYZ" # only used for registering collections

ENDPOINT_ID="XYZ" # globus compute endpoint at nersc 
ENDPOINT_ID_REMOTE="XYZ" # globus compute endpoint on remote machine

SOURCE_ID="XYZ" # endpoint for NERSC transfer collection (Perlmutter DTN to access scratch) 
DESTINATION_ID="XYZ" # transfer collection endpoint on remote machine 

COLLECTION_BASE_PATH="/path/to/location" # the base path of the collection on NERSC so you can mount the container (I use a pscratch path)
RUN_PATH_REMOTE="/path/to/location"
RUN_PATH="/path/to/location"

# register the functions by running the scripts in compute_functions and write the ids here
FUNCTION_ID_QGRAPH="XYZ"
FUNCTION_ID_INGEST="XYZ"
FUNCTION_ID_PIPETASK="XYZ"
FUNCTION_ID_OUTPUTS="XYZ"

FLOW_ID="XYZ" # register the flow and write the id here

STAGING_PATH="/path/to/location" #staging path on nersc for transfer
TRANSFER_PATH="/path/to/location" #location on remote machine to transfer to 

BUTLER_PATH="/path/to/location" # butler path (not config file) on NERSC
BUTLER_PATH_REMOTE="/path/to/location" # butler path (not config file) on remote machine

PIPE_YAML="/path/to/file" # yaml file location on NERSC
PIPE_YAML_REMOTE="/path/to/file" # yaml file location on remote machine

OUTPUT_COLL="u/yourname/yourcoll" # collection name for your outputs
QGRAPH_NAME="/path/to/qgraph/output" # on nersc
INPUT_COLLS="u/me/mycollection1,u/me/mycollection2" # input collections
INPUT_SUFFIX="test" #suffix to append for ingestions, should be different each time
DATASET_PARAMS="skymap='DC2_cells_v1' AND tract=2534 AND patch=62" #example dataset restrictions

OUTPUT_PATH_FINAL="/path/to/keep/outputs" # location on NERSC you'd like to transfer the outputs back to

"""
USERNAME = os.getenv("USERNAME")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")
ENDPOINT_ID_REMOTE = os.getenv("ENDPOINT_ID_REMOTE")


SOURCE_ID = os.getenv("SOURCE_ID")
DESTINATION_ID = os.getenv("DESTINATION_ID")

COLLECTION_BASE_PATH = os.getenv("COLLECTION_BASE_PATH")
RUN_PATH_REMOTE = os.getenv("RUN_PATH_REMOTE")
RUN_PATH = os.getenv("RUN_PATH")

FUNCTION_ID_QGRAPH = os.getenv("FUNCTION_ID_QGRAPH")
FUNCTION_ID_INGEST = os.getenv("FUNCTION_ID_INGEST")
FUNCTION_ID_PIPETASK = os.getenv("FUNCTION_ID_PIPETASK")
FUNCTION_ID_OUTPUTS = os.getenv("FUNCTION_ID_OUTPUTS")

FLOW_ID = os.getenv("FLOW_ID")

STAGING_PATH = os.getenv("STAGING_PATH")
TRANSFER_PATH = os.getenv("TRANSFER_PATH")

BUTLER_PATH = os.getenv("BUTLER_PATH")
BUTLER_PATH_REMOTE = os.getenv("BUTLER_PATH_REMOTE")

PIPE_YAML = os.getenv("PIPE_YAML")
PIPE_YAML_REMOTE = os.getenv("PIPE_YAML_REMOTE")

OUTPUT_COLL = os.getenv("OUTPUT_COLL")
QGRAPH_NAME = os.getenv("QGRAPH_NAME")
INPUT_COLLS = os.getenv("INPUT_COLLS")
INPUT_SUFFIX = os.getenv("INPUT_SUFFIX")
DATASET_PARAMS = os.getenv("DATASET_PARAMS")

OUTPUT_PATH_FINAL = os.getenv("OUTPUT_PATH_FINAL")


# Error if env variables are not set

if not USERNAME: raise EnvironmentError("USERNAME environment variable is not set.")
if not ENDPOINT_ID: raise EnvironmentError("ENDPOINT_ID environment variable is not set.")
if not ENDPOINT_ID_REMOTE: raise EnvironmentError("ENDPOINT_ID_REMOTE environment variable is not set.")
if not SOURCE_ID: raise EnvironmentError("SOURCE_ID environment variable is not set.")
if not DESTINATION_ID: raise EnvironmentError("DESTINATION_ID environment variable is not set.")

if not COLLECTION_BASE_PATH: raise EnvironmentError("COLLECTION_BASE_PATH environment variable is not set.")
if not RUN_PATH_REMOTE: raise EnvironmentError("RUN_PATH_REMOTE environment variable is not set.")
if not RUN_PATH: raise EnvironmentError("RUN_PATH environment variable is not set.")

if not FUNCTION_ID_QGRAPH: raise EnvironmentError("FUNCTION_ID_QGRAPH environment variable is not set.")
if not FUNCTION_ID_INGEST: raise EnvironmentError("FUNCTION_ID_INGEST environment variable is not set.")
if not FUNCTION_ID_PIPETASK: raise EnvironmentError("FUNCTION_ID_PIPETASK environment variable is not set.")
if not FUNCTION_ID_OUTPUTS: raise EnvironmentError("FUNCTION_ID_OUTPUTS environment variable is not set.")

if not FLOW_ID: raise EnvironmentError("FLOW_ID environment variable is not set.")

if not STAGING_PATH: raise EnvironmentError("STAGING_PATH environment variable is not set.")
if not TRANSFER_PATH: raise EnvironmentError("TRANSFER_PATH environment variable is not set.")

if not BUTLER_PATH: raise EnvironmentError("BUTLER_PATH environment variable is not set.")
if not BUTLER_PATH_REMOTE: raise EnvironmentError("BUTLER_PATH_REMOTE environment variable is not set.")

if not PIPE_YAML: raise EnvironmentError("PIPE_YAML environment variable is not set.")
if not PIPE_YAML_REMOTE: raise EnvironmentError("PIPE_YAML_REMOTE environment variable is not set.")

if not OUTPUT_COLL: raise EnvironmentError("OUTPUT_COLL environment variable is not set.")
if not QGRAPH_NAME: raise EnvironmentError("QGRAPH_NAME environment variable is not set.")
if not INPUT_COLLS: raise EnvironmentError("INPUT_COLLS environment variable is not set.")
if not INPUT_SUFFIX: raise EnvironmentError("INPUT_SUFFIX environment variable is not set.")
if not DATASET_PARAMS: raise EnvironmentError("DATASET_PARAMS environment variable is not set.")

if not OUTPUT_PATH_FINAL: raise EnvironmentError("OUTPUT_PATH_FINAL environment variable is not set.")



OUTPUT_PATH = BUTLER_PATH_REMOTE + '/' + OUTPUT_COLL
TRANSFER_PATH2 = TRANSFER_PATH + '/ingestion_files/'

# Define flow input to customize the workflow
flow_input = {
    "input": {
    "source": {
            "id": SOURCE_ID, # Guest Collection UUID for your source transfer endpoint
            "path": STAGING_PATH, # NERSC staging path for file transfer 
            "output_path": OUTPUT_PATH_FINAL #NERSC final path for outputs 
        },
        "destination": {
            "id": DESTINATION_ID, # Guest Collection UUID for your destination transfer endpoint
            "path": TRANSFER_PATH, # Path on remote machine to copy to 
            "path2": TRANSFER_PATH2, # Path where the ingestion files are kept
            "output_path": OUTPUT_PATH, # Path on remote machine where files need to be copied from (Butler path)
        },

        "quantumgraph": {
            "endpoint": ENDPOINT_ID, # Globus Compute endpoint UUID for the computation
            "function": FUNCTION_ID_QGRAPH, # Globus Compute function UUID for the computation
            "arguments": {
                "collection_base_path": COLLECTION_BASE_PATH, # Full path to the base of the Globus collection
                "run_path": RUN_PATH, 
                "transfer_path": TRANSFER_PATH,
                "butler_path": BUTLER_PATH,
                "staging_path": STAGING_PATH,
                "pipe_yaml": PIPE_YAML,
                "output_coll": OUTPUT_COLL,
                "qgraph_name": QGRAPH_NAME,
                "input_colls": INPUT_COLLS,
                "dataset": DATASET_PARAMS,
            }
        },
        "ingestdata": {
            "endpoint": ENDPOINT_ID_REMOTE, # Globus Compute endpoint UUID for the computation
            "function": FUNCTION_ID_INGEST, # Globus Compute function UUID for the computation
            "arguments": {
                "run_path": RUN_PATH_REMOTE, # Full path to the base of the Globus collection
                "butler_path": BUTLER_PATH_REMOTE,
                "transfer_path": TRANSFER_PATH,
                "username": USERNAME,
                "input_suffix": INPUT_SUFFIX,
            }
        },
        "runpipetask": {
            "endpoint": ENDPOINT_ID_REMOTE, # Globus Compute endpoint UUID for the computation
            "function": FUNCTION_ID_PIPETASK, # Globus Compute function UUID for the computation
            "arguments": {
                "run_path": RUN_PATH_REMOTE,
                "butler_path": BUTLER_PATH_REMOTE,
                "transfer_path": TRANSFER_PATH,
                "pipe_yaml": PIPE_YAML_REMOTE,
                "input_suffix": INPUT_SUFFIX,
                "output_coll": OUTPUT_COLL,
                "dataset": DATASET_PARAMS,
                "username": USERNAME,
            }
        },
        "check_outputs": {
            "endpoint": ENDPOINT_ID_REMOTE, # Globus Compute endpoint UUID for the computation
            "function": FUNCTION_ID_OUTPUTS, # Globus Compute function UUID for the computation
            "arguments": {
                "run_path": RUN_PATH_REMOTE, # Full path to the base of the Globus collection
                "butler_path": BUTLER_PATH_REMOTE,
                "transfer_path": TRANSFER_PATH,
                "output_coll": OUTPUT_COLL,
                "final_path": OUTPUT_PATH_FINAL,
            }

        },

    }
}

specific_flow_client = SpecificFlowClient(
    flow_id=FLOW_ID,
    app=UserApp(
        client_id=AUTH_CLIENT_ID,
        app_name="lsst-dest-flow-app"
    )
)

# Start the flow
run = specific_flow_client.run_flow(
    body=flow_input,
    label="LSST-DESC-test"
)

# Collect the run UUID
run_id = run["run_id"]
print(f"\nRun ID: {run_id}")
print(f"Check status at: https://app.globus.org/runs/{run_id}/logs\n")
