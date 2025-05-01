import globus_compute_sdk
from dotenv import load_dotenv
import os

# Load UUIDs
load_dotenv()
function_id = os.getenv("FUNCTION_ID")
endpoint_id = os.getenv("ENDPOINT_ID")

# Create Compute executor
gcc = globus_compute_sdk.Client()
gce = globus_compute_sdk.Executor(client=gcc, endpoint_id=endpoint_id)

# Run function and extract the future object
# Alternatively, for long-duration tasks, gcc client can be used to recover a task UUID and query its status later
future = gce.submit_to_registered_function(function_id)

# Wait and print results
result = future.result()
print(result)