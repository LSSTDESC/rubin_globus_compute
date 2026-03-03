#!/bin/bash/python

"""
- AI generated docstring to explain what thi is doing, not checked yet. 

Extract expected output dataset types and data IDs from a saved QuantumGraph.

This script reads a serialized LSST QuantumGraph and determines all
dataset types produced by the pipeline (i.e., quantum outputs).
For each output dataset type, it collects the corresponding DataIds
referenced in the graph.

The script writes the following files into a specified staging directory:

1. ``output_types.txt``  
   A plain-text list of unique output dataset type names.

2. ``<dataset_type>_outlist.pkl.gz``  
   A gzipped pickle file containing the sorted list of DataIds expected
   for that dataset type.

These files are intended for downstream validation steps that check
whether all expected pipeline outputs were successfully produced.

Command-line arguments
----------------------
1. staging_path : str
   Directory where output summary files will be written.

2. qgraph_name : str
   Path to the saved ``.qgraph`` file to analyze.
"""

import numpy as np
from lsst.pipe.base import QuantumGraph
from lsst.resources import ResourcePath
from pathlib import Path
import sys
import gzip, pickle

staging_path = sys.argv[1]
qgraph_name = sys.argv[2]

QGRAPH = ResourcePath(qgraph_name)
qg = QuantumGraph.load(QGRAPH)

dataset_types = set()
for qnode in qg:
    for refs in qnode.quantum.outputs.values():
        for ref in refs:
           dataset_types.add(ref.datasetType.name)

np.savetxt(staging_path + "/output_types.txt",np.array(list(dataset_types)), fmt="%s")

output_refs={}
for dataset_type in dataset_types:
    output_refs[dataset_type] = set()
    for qnode in qg:
        for ref in qnode.quantum.outputs.get(dataset_type, []):
            output_refs[dataset_type].add(ref.dataId)
    output_refs[dataset_type] = sorted(output_refs[dataset_type])
    with gzip.open(staging_path + "/" + dataset_type + "_outlist.pkl.gz", "wb") as f:
        pickle.dump(output_refs[dataset_type], f, protocol=pickle.HIGHEST_PROTOCOL)


