from globus_sdk import FlowsClient, UserApp

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

resp = flows_client.list_flows()

for f in resp["flows"]:
    print("Flow ID:", f["id"])
    print("Title:", f.get("title"))
    print("Subtitle:", f.get("subtitle"))
    print("Owner:", f.get("flow_owner"))
    print("Definition version:", f.get("definition", {}).get("version"))
    print("-" * 40)

