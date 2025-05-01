# Start from a release LSST stack image.
FROM ghcr.io/lsst/scipipe:al9-w_2025_17

# Information about image.
ARG BUILD_DATE
LABEL maintainer="https://github.com/lsstdesc/rubin_globus_compute"
LABEL description="A Docker image for running the Rubin Science Piplines on Globus Compute."
LABEL version="latest"
LABEL build_date=$BUILD_DATE

WORKDIR /home/lsst

# Clone this repo.
RUN git clone https://github.com/lsstdesc/rubin_globus_compute

# Install Globus Compute endpoint software during development
# Only need when Globus Compute directly executes functions within the container
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip &&\
    python3 -m pip install globus-compute-endpoint

# Make a script to activate the LSST stack
RUN echo "source /opt/lsst/software/stack/loadLSST.bash" >> .bashrc &&\
    echo "setup lsst_distrib" >> .bashrc
