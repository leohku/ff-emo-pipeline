#!/bin/sh

export BASE_DATA_PATH="/home/leoho/repos/pipeline/test-data/"

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