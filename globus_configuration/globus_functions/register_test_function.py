import globus_compute_sdk

# Test function to be executed inside the container
def test_inside():

    # Import the necessary python packages
    import subprocess

    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted
    # ALCF would not allow arbitrary code execution
    commands = [
        "source ./setup_rubin-env.sh",
        "butler create test_from_globus_compute"
    ]

    # Define subprocess arguments
    kwargs = {
        "shell": True, 
        "executable": "/bin/bash",
        "check": True
    }

    # For each command line ...
    for command in commands:
        try:
            subprocess.run(command, **kwargs)
        except subprocess.CalledProcessError as e:
            return f"Error: while processing the following command: {command} -> {e}"
        
    # Return success message if everything worked
    return "All commands ran successfully."

# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# # Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(test_inside)

# # Write function UUID in a file
uuid_file_name = "uuid_test_inside_function.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print("Function registered with UUID -", COMPUTE_FUNCTION_ID)
print("The UUID is stored in " + uuid_file_name + ".")
print("")