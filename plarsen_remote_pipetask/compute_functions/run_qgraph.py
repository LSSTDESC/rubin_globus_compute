import globus_compute_sdk

def run_qgraph(collection_base_path=None, run_path=None, butler_path=None, transfer_path=None, staging_path=None, pipe_yaml=None, output_coll=None, qgraph_name=None, input_colls=None, dataset=None):
    """
    Generate a quantum graph inside a containerized LSST environment, 
    create a list of expected inputs and outputs, and transfer the inputs 
    to a staging area for remote copy. 

    Parameters
    ----------
    collection_base_path : str
        Filesystem path that will be mounted into the container via
        ``--volume``. This path must exist on the host machine and be
        writable by the container.

    run_path : str
        Directory containing local validation scripts 
        ``check_file_list.py`` and ``check_file_list_output.py``.

    butler_path : str
        Path to the Butler repository used as input for QuantumGraph
        construction.

    transfer_path: str
        Path on remote machine where transfer will take place.

    staging_path: str
        Path on local machine where files will be copied for transfer. 

    pipe_yaml : str
        Path to the pipeline YAML definition passed to
        ``pipetask qgraph -p``.

    output_coll : str
        Butler output collection name for the generated QuantumGraph.
        Example: ``"u/<username>/run_test01"``.

    qgraph_name : str
        Filename for the saved QuantumGraph (passed to
        ``--save-qgraph``).

    input_colls : str
        Comma-separated list of Butler input collections passed to
        ``pipetask qgraph -i``.
        Example:
        ``"u/<username>/ingest_raw,u/<username>/calib"``.

    dataset : str
        Data query expression passed to ``pipetask qgraph -d``.
        Example:
        ``"skymap='DC2_cells_v1' AND tract=2534 AND patch=62"``.

    Returns
    -------
    dict
        Dictionary containing:
        - ``returncode`` : int
            Exit status from the container execution.
        - ``stdout`` : str
            Truncated standard output from the container run.
        - ``stderr`` : str
            Truncated standard error from the container run.
        - ``cmd`` : str
            Full Shifter command executed (useful for debugging).

    Raises
    ------
    Exception
        If required inputs are invalid or required local paths do not exist.
    """
    # Import the necessary python packages
    import subprocess
    import re
    import os
    import shlex

    # Validate function inputs
    if not isinstance(collection_base_path, str):
        raise Exception("Error: 'collection_base_path' parameter should be provided as a string.")
    if not isinstance(run_path, str):
        raise Exception("Error: 'run_path' parameter should be provided as a string.")
    if not isinstance(butler_path, str):
        raise Exception("Error: 'butler_path' parameter should be provided as a string.")
    if not isinstance(staging_path, str):
        raise Exception("Error: 'staging_path' parameter should be provided as a string.")
    if not isinstance(transfer_path, str):
        raise Exception("Error: 'transfer_path' parameter should be provided as a string.")
    if not isinstance(pipe_yaml, str):
        raise Exception("Error: 'pipe_yaml' parameter should be provided as a string.")
    if not isinstance(output_coll, str):
        raise Exception("Error: 'output_coll' parameter should be provided as a string.")
    if not isinstance(qgraph_name, str):
        raise Exception("Error: 'qgraph_name' parameter should be provided as a string.")
    if not isinstance(input_colls, str):
        raise Exception("Error: 'input_colls' parameter should be provided as a string.")
    if not isinstance(dataset, str):
        raise Exception("Error: 'dataset' parameter should be provided as a string.")
    
    if not os.path.isdir(collection_base_path):
        raise Exception("Error: 'collection_base_path' must exist.")        
    if not os.path.isdir(run_path):
        raise Exception("Error: 'run_path' must exist.")
    if not os.path.isdir(butler_path):
        raise Exception("Error: 'butler_path' must exist.")
    if not os.path.isdir(staging_path):
        raise Exception("Error: 'staging_path' must exist.")
    if not os.path.isfile(pipe_yaml):
        raise Exception("missing pipeline yaml file")
    if not re.fullmatch(r"[A-Za-z0-9_./-]+(,[A-Za-z0-9_./-]+)*", input_colls):
        raise Exception("input_colls has illegal characters")
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", output_coll):
        raise Exception("output_coll has illegal characters")

    
    collection_base_path = shlex.quote(collection_base_path)
    run_path = shlex.quote(run_path)
    butler_path = shlex.quote(butler_path)
    staging_path = shlex.quote(staging_path)
    transfer_path = shlex.quote(transfer_path)
    pipe_yaml = shlex.quote(pipe_yaml)
    qgraph_name = shlex.quote(qgraph_name)
    dataset = shlex.quote(dataset)
    input_colls = shlex.quote(input_colls)
    output_coll = shlex.quote(output_coll)


    
    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = f"""
    source /opt/lsst/software/stack/loadLSST.bash
    setup lsst_distrib
    eups list lsst_distrib
    pipetask qgraph -b {butler_path} -p {pipe_yaml} -o {output_coll} --save-qgraph {qgraph_name} -i {input_colls} -d {dataset}
    python {run_path}/check_file_list.py {staging_path} {butler_path} {transfer_path} {qgraph_name}
    python {run_path}/check_file_list_output.py {staging_path} {butler_path} {transfer_path} {qgraph_name}
    """

    # Define the Apptainer command to be executed on the compute node
    # Make sure to bind the Globus collection to allow the container to write on the filesystem
    one_line_command = " && ".join(line.strip() for line in commands.strip().splitlines() if line.strip())
    shifter_command = f"shifter --image=lsstsqre/centos:7-stack-lsst_distrib-w_2024_42  --volume {collection_base_path}:/output -- /bin/bash -lc {shlex.quote(one_line_command)}"



    result = subprocess.run(
        shifter_command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return {
        "returncode": result.returncode,
        "stdout": (result.stdout or "")[-20000:],  # trim to avoid size limits
        "stderr": (result.stderr or "")[-20000:],
        "cmd": shifter_command,
    }


# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# # Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(test)

# # Write function UUID in a file
uuid_file_name = "uuid_flow_function_run_qgraph.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print(f"\nFunction registered with UUID - {COMPUTE_FUNCTION_ID}")
print(f"The UUID is stored in {uuid_file_name}.\n")

