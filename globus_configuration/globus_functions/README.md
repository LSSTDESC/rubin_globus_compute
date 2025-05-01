# Globus Compute Function Registration

This folder provides instructions on how to execute command lines within the containers using Globus Compute. Requests to execute Globus Compute functions will be sent to the Globus Compute server, which will relay the request down to the Compute endpoint running on the HPC cluster.

**Note**: Every command below should be executed within your python virtual environment (see README in the previous `globus_configuration` folder).

# Register Function

Look inside the `register_*.py` files for examples on how to define and register functions. Register a function by executing the python file:
```bash
python register_test_function.py
```

This should print a registered function UUID, which is also stored in the `uuid_test_inside_function.txt` file.