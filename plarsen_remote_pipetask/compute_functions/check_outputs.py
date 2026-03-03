import globus_compute_sdk


def check_outputs(run_path=None, butler_path=None, transfer_path=None, output_coll=None, final_path=None):
    """
    Check pipeline outputs on a remote machine.

    This function runs a local ``check_outputs_flow`` script to 
    check if the expected outputs can be found in the Butler repo. 
    This returns 0 if successful, and 1 if any files are missing.
    If successful, it then creates a file of ingestion commands for
    each datatype relative to a ``final_path`` on the local machine. 

    Parameters
    ----------
    run_path : str
        Directory from which to execute the check. A ``loadLSST.sh`` file
        and ``check_outputs_flow.py`` must exist in this directory.

    butler_path : str
        Path to the Butler repository containing the pipeline outputs
        to be validated.

    transfer_path : str
        Directory containing transferred intermediate files or metadata
        used by ``check_outputs_flow.py``.

    output_coll : str
        Butler output collection to validate.
        Example: ``"u/<username>/run_test01"``.
    
    final_path : str
        Final destination path (typically remote) where validated outputs
        will eventually be transferred. This path is not checked for local
        existence within this function.

    Returns
    -------
    dict
        Dictionary containing:
        - ``returncode`` : int
            Exit status returned by ``check_outputs_flow.py``.
            A value of ``0`` typically indicates success.
        - ``stdout`` : str
            Truncated standard output from the check process.
        - ``stderr`` : str
            Truncated standard error from the check process.

    Raises
    ------
    Exception
        If required inputs are invalid or required local directories/files
        do not exist.
    
    """
    # Import the necessary python packages
    import subprocess
    import os
    import shlex
    import re

    # Validate function inputs
    if not isinstance(run_path, str):
        raise Exception("Error: 'run_path' parameter should be provided as a string.")
    if not isinstance(butler_path, str):
        raise Exception("Error: 'butler_path' parameter should be provided as a string.")
    if not isinstance(transfer_path, str):
        raise Exception("Error: 'transfer_path' parameter should be provided as a string.")
    if not isinstance(output_coll, str):
        raise Exception("Error: 'output_coll' parameter should be provided as a string.")
    if not isinstance(final_path, str):
        raise Exception("Error: 'final_path' parameter should be provided as a string.")
    
    if not os.path.isdir(run_path):
        raise Exception("Error: 'run_path' must exist.")
    if not os.path.isdir(butler_path):
        raise Exception("Error: 'butler_path' must exist.")
    if not os.path.isdir(transfer_path):
        raise Exception("Error: 'transfer_path' must exist.")
    if not os.path.isfile(os.path.join(run_path, "check_outputs_flow.py")):
        raise Exception("missing check_outputs_flow.py")

    if not re.fullmatch(r"[A-Za-z0-9_./-]+", output_coll):
        raise Exception("output_coll has illegal characters")
        
    run_path = shlex.quote(run_path)
    butler_path = shlex.quote(butler_path)
    transfer_path = shlex.quote(transfer_path)
    final_path = shlex.quote(final_path)
    output_coll = shlex.quote(output_coll)

    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = f"""
    cd {run_path}
    source {run_path}/loadLSST.sh
    setup lsst_distrib
    
    python {run_path}/check_outputs_flow.py {butler_path} {transfer_path} {output_coll} {final_path}
    """

    result = subprocess.run(
        ["bash", "-lc", commands],
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    return {
        "returncode": int(result.returncode),
        "stdout": (result.stdout or "")[-20000:],  # trim to avoid size limits
        "stderr": (result.stderr or "")[-20000:],
    }

# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# # Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(check_outputs)

# # Write function UUID in a file
uuid_file_name = "uuid_flow_function_check_outputs.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print(f"\nFunction registered with UUID - {COMPUTE_FUNCTION_ID}")
print(f"The UUID is stored in {uuid_file_name}.\n")
