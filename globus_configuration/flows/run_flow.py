from globus_sdk import SpecificFlowClient, UserApp
from dotenv import load_dotenv
import os

# Public Globus thick client for authentication
AUTH_CLIENT_ID = "f818e8c5-61ba-4f70-8237-a8e69f266ae7"

# Load UUIDs
load_dotenv()
ENDPOINT_ID = os.getenv("ENDPOINT_ID")
FUNCTION_ID = os.getenv("FUNCTION_ID")
SIF_SING_PATH = os.getenv("SIF_SING_PATH")
FLOW_ID = os.getenv("FLOW_ID")
SOURCE_ID = os.getenv("SOURCE_ID")
SOURCE_PATH = os.getenv("SOURCE_PATH")
DESTINATION_ID = os.getenv("DESTINATION_ID")
DESTINATION_PATH = os.getenv("DESTINATION_PATH")
DESTINATION_COLLECTION_BASE_PATH = os.getenv("DESTINATION_COLLECTION_BASE_PATH")

# Error if env variables are not set
if not ENDPOINT_ID: raise EnvironmentError("ENDPOINT_ID environment variable is not set.")
if not FUNCTION_ID: raise EnvironmentError("FUNCTION_ID environment variable is not set.")
if not SIF_SING_PATH: raise EnvironmentError("SIF_SING_PATH environment variable is not set.")
if not FLOW_ID: raise EnvironmentError("FLOW_ID environment variable is not set.")
if not SOURCE_ID: raise EnvironmentError("SOURCE_ID environment variable is not set.")
if not SOURCE_PATH: raise EnvironmentError("SOURCE_PATH environment variable is not set.")
if not DESTINATION_ID: raise EnvironmentError("DESTINATION_ID environment variable is not set.")
if not DESTINATION_PATH: raise EnvironmentError("DESTINATION_PATH environment variable is not set.")
if not DESTINATION_COLLECTION_BASE_PATH: raise EnvironmentError("DESTINATION_COLLECTION_BASE_PATH environment variable is not set.")

# Define flow input to customize the workflow
flow_input = {
    "input": {
        "source": {
            "id": SOURCE_ID, # Guest Collection UUID for your source transfer endpoint
            "path": SOURCE_PATH # Path to the folder where the input files are (from the base of the collection)
                                # Needs to end with "/"
        },
        "destination": {
            "id": DESTINATION_ID, # Guest Collection UUID for your destination transfer endpoint
            "path": DESTINATION_PATH # Path where the folder will be transfered to (from the base of the collection)
                                     # Needs to end with "/"
        },
        "compute": {
            "endpoint": ENDPOINT_ID, # Globus Compute endpoint UUID for the computation
            "function": FUNCTION_ID, # Globus Compute function UUID for the computation
            "arguments": {
                "sif_sing_path": SIF_SING_PATH, # Full path to the .sif or .sing container file
                "collection_base_path": DESTINATION_COLLECTION_BASE_PATH, # Full path to the base of the Globus collection
                "destination_path": DESTINATION_PATH #Path relative to the Globus collection where results will be written
            }
        }
    }
}

# Create authenticated Flows client
# NOTE: This can be changed to use client's secrets to avoid having to authenticate
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