from globus_sdk import FlowsClient, UserApp

flow_definition = {
    "Comment": "LSST-DESC Flow Definition",
    "StartAt": "QuantumGraph",
    "States": {
        "QuantumGraph": {
            "Comment": "Run quantum graph analysis.",
            "Type": "Action",
            "ActionUrl": "https://compute.actions.globus.org/",
            "Parameters": {
                "endpoint.$": "$.input.quantumgraph.endpoint",
                "function.$": "$.input.quantumgraph.function",
                "kwargs.$": "$.input.quantumgraph.arguments"
            },
            "ResultPath": "$.QuantumGraph_output",
            "WaitTime": 172800,
            "Next": "TransferInputs"
        },
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
            "WaitTime": 172800,
            "Next": "IngestData"
        },
        "IngestData": {
            "Comment": "Ingest data on local machine.",
            "Type": "Action",
            "ActionUrl": "https://compute.actions.globus.org/",
            "Parameters": {
                "endpoint.$": "$.input.ingestdata.endpoint",
                "function.$": "$.input.ingestdata.function",
                "kwargs.$": "$.input.ingestdata.arguments"
            },
            "ResultPath": "$.IngestData_output",
            "WaitTime": 172800,
            "Next": "InitCount"
        },

        "InitCount": {
                "Type": "Pass",
                "Result": { "attempt": 0 , "rc": 1},
                "ResultPath": "$.loop",
                "Next": "RunPipetask"
        },
        
        "RunPipetask": {
            "Comment": "Run pipetask on local machine.",
            "Type": "Action",
            "ActionUrl": "https://compute.actions.globus.org/",
            "Parameters": {
                "endpoint.$": "$.input.runpipetask.endpoint",
                "function.$": "$.input.runpipetask.function",
                "kwargs.$": "$.input.runpipetask.arguments"
            },
            "ResultPath": "$.RunPipetask_output",
            "WaitTime": 172800,
            "Next": "CheckOutput"
        },
        
        "CheckOutput": {
            "Comment": "Check outputs on local machine.",
            "Type": "Action",
            "ActionUrl": "https://compute.actions.globus.org/",
            "Parameters": {
                "endpoint.$": "$.input.check_outputs.endpoint",
                "function.$": "$.input.check_outputs.function",
                "kwargs.$": "$.input.check_outputs.arguments"
            },
            "ResultPath": "$.CheckOutput_output",
            "WaitTime": 172800,
            "Next": "IterCount"
        },
        
        "IterCount": {
            "Comment": "Update count of attempts.",
            "Type": "ExpressionEval",
            "Parameters": {
            "attempt.=": "loop.attempt + 1",
            "rc.$": "$.CheckOutput_output.details.result[0].returncode"
          },
          "ResultPath": "$.loop",
          "Next": "RerunChoice"
        },
        
        "RerunChoice": {
            "Comment": "Decide whether to rerun pipetask.",
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.loop.rc",
                    "NumericEquals": 0,
                    "Next": "Done"
                },
                {
                    "And": [
                        {"Variable": "$.loop.rc", "NumericEquals": 1},
                        {"Variable": "$.loop.attempt", "NumericLessThan": 3}
                    ],
                    "Next": "Compute3"
                }
            ],
            "Default": "FailTooManyTries"
        },

            "Done": { "Type": "Pass" ,
                      "Next": "TransferOutputs"
                    },

            "FailTooManyTries": {
                "Type": "Fail",
                "Cause": "Missing outputs, 3 attempts done" 
            },
        "TransferOutputs": {
            "Comment": "Transfer folder from destination to source where they will be ingested.",
            "Type": "Action",
            "ActionUrl": "https://transfer.actions.globus.org/transfer",
            "Parameters": {
                "source_endpoint.$": "$.input.destination.id",
                "destination_endpoint.$": "$.input.source.id",
                "DATA": [
                    {
                        "source_path.$": "$.input.destination.output_path",
                        "destination_path.$": "$.input.source.output_path",
                        "recursive": True,
                    }
                ]
            },
            "ResultPath": "$.TransferOutputs_output",
            "WaitTime": 172800,
          "Next": "TransferOutputs2"
        },
        "TransferOutputs2": {
            "Comment": "Transfer ingestion details.",
            "Type": "Action",
            "ActionUrl": "https://transfer.actions.globus.org/transfer",
            "Parameters": {
                "source_endpoint.$": "$.input.destination.id",
                "destination_endpoint.$": "$.input.source.id",
                "DATA": [
                    {
                        "source_path.$": "$.input.destination.path_ingestion",
                        "destination_path.$": "$.input.source.path",
                        "recursive": True,
                    }
                ]
            },
            "ResultPath": "$.TransferOutputs2_output",
            "WaitTime": 172800,
            "End": True
        },

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
