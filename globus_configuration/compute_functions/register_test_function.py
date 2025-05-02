import globus_compute_sdk

# Test function when workers are deployed inside of the container
def test():

    # Import the necessary python packages
    import subprocess

    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = """
    source /opt/lsst/software/stack/loadLSST.bash
    setup lsst_distrib
    eups list lsst_distrib
    command -v python
    """

    # Define subprocess arguments
    kwargs = {
        "shell": True, 
        "executable": "/bin/bash",
        "check": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True
    }

    # Execute the command lines
    try:
        result = subprocess.run(commands, **kwargs)
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
        
    # Return command line output
    return result.stdout

# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# # Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(test)

# # Write function UUID in a file
uuid_file_name = "uuid_test_function.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print("Function registered with UUID -", COMPUTE_FUNCTION_ID)
print("The UUID is stored in " + uuid_file_name + ".")
print("")