import globus_compute_sdk

# Test function when workers are deployed outside of the container
def test(sif_sing_path=None, collection_base_path=None, destination_path=None):
    """
    Test function that will load the LSST/Desc environment and print
    the location of the python executable from within the container.
    
    Argument
    --------
        sif_sing_path (str): Full path to the Apptainer .sif or .sing file
        collection_base_path(str): Full path to the base of the Globus collection
        destination_path(str): Path relative to the Globus collection where results will be written
    """

    # Import the necessary python packages
    import subprocess
    import uuid
    import os

    # Validate function inputs
    if not isinstance(sif_sing_path, str):
        raise Exception("Error: 'sif_sing_path' parameter should be provided as a string.")
    if not isinstance(collection_base_path, str):
        raise Exception("Error: 'collection_base_path' parameter should be provided as a string.")
    if not isinstance(destination_path, str):
        raise Exception("Error: 'destination_path' parameter should be provided as a string.")
    
    # Create a unique output folder name
    folder_name = f"test_repo_{str(uuid.uuid4())}"

    # Build the path of the output folder relative to the base of the Globus collection
    if destination_path.startswith("/"):
        destination_path = destination_path[1:]
    output_path = os.path.join(destination_path, folder_name)

    # Build the full path of the output folder from the HPC's filesystem perspective
    full_output_path = os.path.join(collection_base_path, output_path)

    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = f"""
    source /opt/lsst/software/stack/loadLSST.bash
    setup lsst_distrib
    eups list lsst_distrib
    mkdir {full_output_path}
    """

    # Define subprocess arguments
    kwargs = {
        "shell": True, 
        "check": True,
        "text": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "executable": "/bin/bash"
    }

    # Define the Apptainer command to be executed on the compute node
    # Make sure to bind the Globus collection to allow the container to write on the filesystem
    one_line_command = " && ".join(line.strip() for line in commands.strip().splitlines() if line.strip())
    apptainer_command = f"apptainer exec --fakeroot -B {collection_base_path}:{collection_base_path} {sif_sing_path} bash -c '{one_line_command}'"

    # Execute the command lines
    try:
        result = subprocess.run(apptainer_command, **kwargs)
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Error: {e}")
        
    # Return the output folder path relative to the base of the Globus collection
    return {
        "output_path": output_path
    }


# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# # Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(test)

# # Write function UUID in a file
uuid_file_name = "uuid_flow_function.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print(f"\nFunction registered with UUID - {COMPUTE_FUNCTION_ID}")
print(f"The UUID is stored in {uuid_file_name}.\n")
