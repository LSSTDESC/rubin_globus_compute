# Globus Configuration

This folder provides instructions on how to wrap LSST/Desc containers with Globus Compute for remote execution on the ALCF Polaris HPC cluster. Below are instructions regarding virtual environments. Instructions on how to configure Compute endpoints and execute Compute functions are provided in the [compute endpoints](./compute_endpoints/) and [compute functions](./compute_functions/) folders.

## Create Your Virtual Environment

When configuring Globus Compute endpoints and registering/running Globus Compute functions, it is recommended to use environments that always have the same python version. Otherwise you may encounter issues related to serialization. It is important to note that such an environment is separate from the LSST/Desc container environment. It is only needed to operate Globus Compute.

If the functions are to be executed within the container directly (i.e. if the compute workers are deployed within the container), make sure that the python version where you register your function matches the version used in the container. To verify which python version is used in the container, first acquire a compute node:
```bash
qsub -I -A <your-compute-allocation> -q debug -l select=1 -l walltime=01:00:00 -l filesystems=home:grand:eagle
```

Then, follow the [Apptainer Setup](https://docs.alcf.anl.gov/polaris/containers/containers/) instructions, and execute the following Apptainer command:
```bash
apptainer exec --fakeroot /full/path/to/your/.sing-or-.sif-file python3 --version
```

### Example with Miniconda3

Install Miniconda3 in your home directory (see more installation files [here]((https://repo.anaconda.com/miniconda/))):
```bash
MINICONDA_FILE="Miniconda3-latest-Linux-x86_64.sh"
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/${MINICONDA_FILE} -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

Create a virtual environment with a specific python version (here `3.9.21` from current Dockerfile):
```bash
~/miniconda3/bin/conda create -y -n gc-env python=3.9.21
```

Activate your virtual environment:
```bash
source ~/miniconda3/bin/activate ~/miniconda3/envs/gc-env
```

Install packages that are required to operate Globus Compute:
```bash
pip install -r requirements.txt
```