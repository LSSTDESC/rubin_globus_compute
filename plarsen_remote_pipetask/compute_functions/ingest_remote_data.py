import globus_compute_sdk

def ingest_data(run_path=None, butler_path=None, transfer_path=None, input_suffix=None, username=None):
    """
    Ingest input data into a Butler repository on a remote machine.

    Parameters
    ----------
    run_path : str
        Path from which to execute the ingestion. A ``loadLSST.sh`` file
        must exist in this directory.

    butler_path : str
        Path to the Butler repository where datasets will be ingested.

    transfer_path : str
        Directory containing transferred files and the ``input_types.txt``
        file describing dataset types to ingest.

    input_suffix : str
        Unique suffix identifying this run. This value is incorporated
        into the output collection names and must be distinct for each run.

    username : str
        Username used to construct Butler collection paths (e.g.,
        ``u/<username>/...``).

    Returns
    -------
    dict
        Dictionary containing:
        - ``returncode`` : int
            Exit status from the ingestion command.
        - ``stdout`` : str
            Truncated standard output from the ingestion process.
        - ``stderr`` : str
            Truncated standard error from the ingestion process.

    Raises
    ------
    Exception
        If required inputs are invalid or required directories do not exist.
    RuntimeError
        If the ingestion command fails (depending on calling context).
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
    if not isinstance(input_suffix, str):
        raise Exception("Error: 'input_suffix' parameter should be provided as a string.")
    if not isinstance(username, str):
        raise Exception("Error: 'username' parameter should be provided as a string.")

    if not os.path.isdir(run_path):
        raise Exception("Error: 'run_path' must exist.")
    if not os.path.isdir(butler_path):
        raise Exception("Error: 'butler_path' must exist.")
    if not os.path.isdir(transfer_path):
        raise Exception("Error: 'transfer_path' must exist.")
    if not os.path.isfile(os.path.join(transfer_path, "input_types.txt")):
        raise Exception("missing input_types.txt")


    # Quote paths for safety
    run_path = shlex.quote(run_path)
    butler_path = shlex.quote(butler_path)
    transfer_path = shlex.quote(transfer_path)

    if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
        raise Exception("username has illegal characters")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", input_suffix):
        raise Exception("input_suffix has illegal characters")


    
    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = f"""
    cd {run_path}
    source {run_path}/loadLSST.sh
    setup lsst_distrib
    for name in $(cat {transfer_path}/input_types.txt); do
        butler ingest-files {butler_path} "$name" u/{username}/ingest_"$name"_{input_suffix} {transfer_path}/"$name"_ingest_table.csv --transfer direct
    done
    """

    result = subprocess.run(
        ["bash", "-lc", commands],
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return {
        "returncode": result.returncode,
        "stdout": (result.stdout or "")[-20000:],  # trim to avoid size limits
        "stderr": (result.stderr or "")[-20000:],
    }

gcc = globus_compute_sdk.Client()

# Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(ingest_data)

# # Write function UUID in a file
uuid_file_name = "uuid_flow_function_ingest_remote_data.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print(f"\nFunction registered with UUID - {COMPUTE_FUNCTION_ID}")
print(f"The UUID is stored in {uuid_file_name}.\n")
