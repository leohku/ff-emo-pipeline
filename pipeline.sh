#!/bin/sh

# PRODUCTION
export BASE_DATA_PATH="/home/leoho/data/pipeline-data/pipeline-data-lambda/"
# TEST
# export BASE_DATA_PATH="/home/leoho/repos/pipeline/test-data-3/"

starting_time=$(date +%s)
echo "Starting UNIX time: "$starting_time

cd 1-emoca
python create-templates.py
python extract-objs-from-video.py
python audio-processing.py
cd ../2-open3d
python template-normalisation.py
python mesh-registration.py
cd ../3-preformer
python template-packing.py
python sentence-packing.py
cd ../4-variance
python variance-extraction.py

ending_time=$(date +%s)
echo "Ending UNIX time: "$ending_time
elapsed_time=$(( $ending_time - $starting_time ))
echo "Elpased seconds: "$elapsed_time