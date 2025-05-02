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

# Install Globus Compute endpoint system-wide (not inside lsst environment to avoid interfering with dependencies)
# Only needed when Globus Compute directly executes functions within the container
USER root
RUN dnf install -y python3 python3-pip && \
    dnf clean all
RUN pip3 install globus-compute-endpoint
USER lsst

# Make a script to activate the LSST stack
RUN echo "source /opt/lsst/software/stack/loadLSST.bash" >> .bashrc &&\
    echo "setup lsst_distrib" >> .bashrc
