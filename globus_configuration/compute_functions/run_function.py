import globus_compute_sdk
from dotenv import load_dotenv
import os

# Load UUIDs
load_dotenv()
FUNCTION_ID = os.getenv("FUNCTION_ID")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")
SIF_SING_PATH = os.getenv("SIF_SING_PATH")

# Create Compute executor
gcc = globus_compute_sdk.Client()
gce = globus_compute_sdk.Executor(client=gcc, endpoint_id=ENDPOINT_ID)

# Run function and extract the future object
# Alternatively, for long-duration tasks, gcc client can be used to recover a task UUID and query its status later
future = gce.submit_to_registered_function(
    FUNCTION_ID,
    kwargs={
        "sif_sing_path": SIF_SING_PATH
    }
)

# Wait and print results
result = future.result()
print(result)
