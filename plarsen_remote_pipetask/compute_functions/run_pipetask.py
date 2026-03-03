import globus_compute_sdk


def run_pipetask(run_path=None, butler_path=None, transfer_path=None, pipe_yaml=None, input_suffix=None, output_coll=None, dataset=None, username=None):
    """
    Run LSST pipetask on a remote machine.

    Parameters
    ----------
    run_path : str
        Path from which to execute the run. A ``loadLSST.sh`` file
        must exist in this directory.

    butler_path : str
        Path to the Butler repository where datasets live.

    transfer_path : str
        Directory containing transferred files and the ``input_types.txt``
        file.

    input_suffix : str
        Unique suffix identifying this run. This value is incorporated
        into the output collection names and must be distinct for each run.

    output_coll : str
        Output collection to write pipeline products into.
        Example: ``"u/<username>/run_test01"``.

    dataset : str
        Data query expression passed to ``pipetask run -d``.
        Example: ``"skymap='DC2_cells_v1' AND tract=2534 AND patch=62"``.

    username : str
        Username used to construct Butler collection paths (e.g.,
        ``u/<username>/...``).

    Returns
    -------
    dict
        Dictionary containing:
        - ``returncode`` : int
            Exit status from the pipetask command.
        - ``stdout`` : str
            Truncated standard output from the pipetask process.
        - ``stderr`` : str
            Truncated standard error from the pipetask process.

    Raises
    ------
    Exception
        If required inputs are invalid or required directories do not exist.
    RuntimeError
        If the pipetask command fails (depending on calling context).
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
    if not isinstance(pipe_yaml, str):
        raise Exception("Error: 'pipe_yaml' parameter should be provided as a string.")
    if not isinstance(input_suffix, str):
        raise Exception("Error: 'input_suffix' parameter should be provided as a string.")
    if not isinstance(output_coll, str):
        raise Exception("Error: 'output_coll' parameter should be provided as a string.")
    if not isinstance(dataset, str):
        raise Exception("Error: 'dataset' parameter should be provided as a string.")
    if not isinstance(username, str):
        raise Exception("Error: 'username' parameter should be provided as a string.")

        
    if not os.path.isdir(run_path):
        raise Exception("Error: 'run_path' must exist.")
    if not os.path.isdir(butler_path):
        raise Exception("Error: 'butler_path' must exist.")
    if not os.path.isdir(transfer_path):
        raise Exception("Error: 'transfer_path' must exist.")
    if not os.path.isfile(pipe_yaml):
        raise Exception("missing pipeline yaml file")
    if not os.path.isfile(os.path.join(transfer_path, "input_types.txt")):
        raise Exception("missing input_types.txt")

    
    run_path = shlex.quote(run_path)
    butler_path = shlex.quote(butler_path)
    transfer_path = shlex.quote(transfer_path)
    pipe_yaml = shlex.quote(pipe_yaml)
    dataset = shlex.quote(dataset)


    if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
        raise Exception("username has illegal characters")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", input_suffix):
        raise Exception("input_suffix has illegal characters")
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", output_coll):
        raise Exception("output_coll has illegal characters")

    
    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = f"""
    cd {run_path}
    source {run_path}/loadLSST.sh
    setup lsst_distrib
    
    input_colls=$(
    awk -v oc="{input_suffix}" '
    NF {{                                  
      coll = "u/{username}/ingest_" $1 "_" oc
      if (out == "") out = coll
      else out = out "," coll
    }}
    END {{ print out }}
    ' {transfer_path}/input_types.txt)
    pipetask run -b {butler_path} -p {pipe_yaml} -o "{output_coll}" -i "$input_colls" -d {dataset} --register-dataset-types --skip-existing -j8
    """

    try:
        result = subprocess.run(
            ["bash", "-lc", commands],
            text=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print("FAILED with return code:", e.returncode)
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise

    return {
        "returncode": result.returncode,
        "stdout": (result.stdout or "")[-20000:],  # trim to avoid size limits
        "stderr": (result.stderr or "")[-20000:],
    }






# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(ingest_data)

# # Write function UUID in a file
uuid_file_name = "uuid_flow_function_run_pipetask.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print(f"\nFunction registered with UUID - {COMPUTE_FUNCTION_ID}")
print(f"The UUID is stored in {uuid_file_name}.\n")

