#!/bin/bash/python

"""
AI-generated docstring, not checked yet!

Stage required input datasets from a QuantumGraph for transfer and ingestion.

This script analyzes a saved LSST QuantumGraph to determine all input
dataset types required by the pipeline (i.e., quantum inputs). For each
input dataset type, it:

1. Identifies all referenced DatasetRefs in the QuantumGraph.
2. Resolves their underlying datastore file locations via Butler.
3. Generates per-dataset-type ingestion tables mapping final output
   paths to the corresponding DataIds.
4. Copies the required file-backed artifacts into a staging directory,
   preserving paths relative to the Butler repository when possible.

The staging directory will contain:

- ``input_types.txt``  
  A list of unique input dataset type names.

- ``<dataset_type>_ingest_table.csv``  
  CSV files describing the files and associated DataIds required for
  Butler ingestion on the remote system.

- A staged copy of all required input files, organized relative to the
  repository root (or preserving absolute structure if not under the repo).

This script is typically used prior to remote execution, enabling
transfer of all necessary input artifacts and metadata.

Command-line arguments
----------------------
1. staging_path : str
   Directory where staging files and ingestion tables will be written.

2. REPO : str
   Path to the Butler repository containing the required input datasets.

3. output_path : str
   Base path on the remote system used to construct final file paths
   in the ingestion tables.

4. qgraph_name : str
   Path to the saved ``.qgraph`` file to analyze.
"""

from lsst.pipe.base import QuantumGraph
from lsst.daf.butler import Butler
from lsst.resources import ResourcePath
from pathlib import Path
import sys
import shutil
import csv
import json
import numpy as np


# copy a symlink to a staging area for transfer
staging_path = sys.argv[1]
REPO = sys.argv[2]
output_path = sys.argv[3] # on remote machine 
qgraph_name = sys.argv[4]


QGRAPH = ResourcePath(qgraph_name)
qg = QuantumGraph.load(QGRAPH)
butler = Butler(REPO)

dataset_types = set()
for qnode in qg:
    for refs in qnode.quantum.inputs.values():
        for ref in refs:
           dataset_types.add(ref.datasetType.name)

np.savetxt(staging_path + "/input_types.txt",np.array(list(dataset_types)), fmt="%s")

input_refs={}
for dataset_type in dataset_types:
    input_refs[dataset_type] = set()
    for qnode in qg:
        for ref in qnode.quantum.inputs.get(dataset_type, []):
            input_refs[dataset_type].add(ref)

file_paths = set()

rows={}
for key in input_refs.keys():
    rows[key] = []
    for ref in input_refs[key]:
        dataid = dict(ref.dataId.mapping)
        for uri in butler.getURIs(ref):
            if isinstance(uri, dict):
                continue  # skip {} and any component maps
            scheme = getattr(uri, "scheme", None)
            file_paths.add(uri.path if scheme == "file" else str(uri))
            src_path = Path(uri.ospath)
            try:
                rel = src_path.relative_to(REPO+'/')
                outpath = Path(output_path) / rel
            except ValueError:
                outpath = Path(output_path) / src_path.name
            rows[key].append({"path": str(outpath), **dataid})


for key in rows.keys():
    table_csv = staging_path + "/" + key+"_ingest_table.csv"
    with open(table_csv, "w", newline="") as f:
        fieldnames = ["path"] + sorted({k for r in rows[key] for k in r.keys() if k != "path"})
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows[key])


file_list = sorted(file_paths)
stage = Path(staging_path)

for src in file_list:
    srcp = Path(src)
    try:
        rel = srcp.relative_to(REPO+'/')
        dst = stage / rel
    except ValueError:
        # fallback: preserve absolute path
        dst = stage / srcp.relative_to("/")

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        continue   # already copied

    shutil.copy2(srcp, dst)


