# Globus Configuration

This folder provides instructions on how to setup Globus Compute to run the Rubin/Desc workflow. Miniconda3 is used to create simple environment to deploy and operate Globus Compute (see below). Examples of compute endpoint configuration are given in the `compute_endpoints` folder. Examples of compute function registrations and usage are given in the `compute_functions` folder.

## Virtual Environment

When configuring Globus Compute endpoints and registering/running Globus Compute functions, it is recommended to use environments that always have the same python version. Otherwise you may encounter issues related to serialization. If the functions are to be executed within the container directly (i.e. if the compute workers are deployed within the container), make sure the function registration is done using the same python version that is available within the container. You can check this version by executing the following:
```bash
apptainer exec --fakeroot /full/path/to/your/file.sing python3 --version
```
If the functions are to be executed from outside of the container via a series of `apptainer exec` commands (i.e. if the compute workers are deployed on the compute node), the python version does not need to match the version within the container.

### Example with Miniconda3

Select the [miniconda installation file]((https://repo.anaconda.com/miniconda/)) that is the most appropriate for your system:
```bash
# This works for Polaris login nodes
MINICONDA_FILE="Miniconda3-latest-Linux-x86_64.sh"
```

Install Miniconda3 in your home directory:
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/${MINICONDA_FILE} -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

Create virtual environment with specific version (here 3.9.19 to match current container):
```bash
~/miniconda3/bin/conda create -y -n gc-env python=3.9.19
```

Activate your virtual environment:
```bash
source ~/miniconda3/bin/activate ~/miniconda3/envs/gc-env
```

Install necessary packages:
```bash
pip install globus-compute-endpoint globus-compute-sdk globus-sdk
pip install python-dotenv
```