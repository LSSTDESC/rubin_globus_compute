from globus_sdk import FlowsClient, UserApp

# 3-step flow definition (Transfer + Compute + Transfer)
flow_definition = {
    "Comment": "LSST-DESC Flow Definition",
    "StartAt": "TransferInputs",
    "States": {
        "TransferInputs": {
            "Comment": "Transfer folder from source to destination where the anaylsis will occur.",
            "Type": "Action",
            "ActionUrl": "https://transfer.actions.globus.org/transfer",
            "Parameters": {
                "source_endpoint.$": "$.input.source.id",
                "destination_endpoint.$": "$.input.destination.id",
                "DATA": [
                    {
                        "source_path.$": "$.input.source.path",
                        "destination_path.$": "$.input.destination.path",
                        "recursive": True,
                    }
                ]
            },
            "ResultPath": "$.TransferInputs_output",
            "WaitTime": 18000,
            "Next": "Compute"
        },
        "Compute": {
            "Comment": "Run analysis at the HPC facility.",
            "Type": "Action",
            "ActionUrl": "https://compute.actions.globus.org/",
            "Parameters": {
                "endpoint.$": "$.input.compute.endpoint",
                "function.$": "$.input.compute.function",
                "kwargs.$": "$.input.compute.arguments"
            },
            "ResultPath": "$.Compute_output",
            "WaitTime": 172800,
            "Next": "TransferResults"
        },
        "TransferResults": {
            "Comment": "Transfer results folder back to the source.",
            "Type": "Action",
            "ActionUrl": "https://transfer.actions.globus.org/transfer",
            "Parameters": {
                "source_endpoint.$": "$.input.destination.id",
                "destination_endpoint.$": "$.input.source.id",
                "DATA": [
                    {
                        "source_path.$": "$.input.destination.path",
                        "destination_path.$": "$.input.source.path",
                        "recursive": True,
                    }
                ]
            },
            "ResultPath": "$.TransferResults_output",
            "WaitTime": 18000,
            "End": True
        }
    }
}

# Public Globus thick client for authentication
AUTH_CLIENT_ID = "f818e8c5-61ba-4f70-8237-a8e69f266ae7"

# Create authenticated Flows client
# NOTE: This can be changed to use client's secrets to avoid having to authenticate
flows_client = FlowsClient(
    app=UserApp(
        client_id=AUTH_CLIENT_ID,
        app_name="lsst-dest-flow-app"
    )
)

# Register flow
flow = flows_client.create_flow(
    title="LSST-DESC Globus Flow demo", 
    definition=flow_definition,
    input_schema={} # This can be set to restric the flow input format
)

# Collect the flow UUID
FLOW_ID = flow["id"]
print(f"\nFlow registered with UUID - {FLOW_ID}")
print(f"https://app.globus.org/flows/{FLOW_ID}")

# # Write flow UUID in a file
uuid_file_name = "uuid_flow.txt"
with open(uuid_file_name, "w") as file:
    file.write(FLOW_ID)
    file.write("\n")
file.close()
print(f"The UUID is stored in {uuid_file_name}.\n")
