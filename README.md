Pipeline for processing MEAD data through EMOCA for FaceFormer training

## Prerequisites

```
conda activate work36_cu11_pipeline
```

## Usage

First ensure the data folder has the following directories initialised

```
MEAD              <- with data
MEAD_EMOCA
MEAD_FACEFORMER
MEAD_OPEN3D
MEAD_PREFORMER
```

Run `nohup ./pipeline.sh > logs/001.log 2>&1 &` to process data.

Alternatively, set your env variable `BASE_DATA_PATH`, then run these Python files in sequence:

```
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
```
