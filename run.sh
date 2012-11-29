#!/bin/bash

# Author: Yuan Du (yd2234@columbia.edu)
# Date: Nov 28, 2012
# Function: get large itemsets and association rules by given min-conf and min-sup
# Usage: sh run.sh <INTEGRATED-DATASET-FILE> <min_sup> <min_conf>

python src/extract_Rule.py "${1}" "${2}" "${3}" output.txt