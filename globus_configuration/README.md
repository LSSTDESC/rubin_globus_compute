# Globus Configuration

This folder includes instructions on how to wrap LSST/Desc containers with Globus Compute for remote execution on the ALCF Polaris HPC cluster. Below are notes regarding virtual environments and Globus accounts. Instructions on how to configure Compute endpoints and execute Compute functions are provided in the [compute endpoints](./compute_endpoints/) and [compute functions](./compute_functions/) folders.

## Globus Account

Make sure you have an active [Globus account](https://app.globus.org/).

## Virtual Environment

When configuring Globus Compute endpoints and registering/executing Globus Compute functions, you should always use an environment that has the same python version, otherwise you may encounter issues related to serialization.

### Example with Miniconda3

If not already done, install Miniconda3 in your home directory (see more installation files [here](https://repo.anaconda.com/miniconda/)):
```bash
MINICONDA_FILE="Miniconda3-latest-Linux-x86_64.sh"
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/${MINICONDA_FILE} -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

Create a virtual environment with a specific python version (here `3.12.4`):
```bash
~/miniconda3/bin/conda create -y -n gc-env python=3.12.4
```

Activate your virtual environment and install the packages that are required to operate Globus Compute:
```bash
source ~/miniconda3/bin/activate ~/miniconda3/envs/gc-env
pip install -r requirements.txt
```