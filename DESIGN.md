Processing Pipeline:

MEAD -> MEAD_EMOCA -> MEAD_OPEN3D -> MEAD_PREFORMER -> MEAD_FACEFORMER

[MEAD_EMOCA STAGE]

// Create template file ✅

MEAD/<M|Wxxx>/video-001/video/front/neutral/level_1/001.mp4
=> grab last frame
=> output image stored in MEAD_EMOCA/template_input/<M|Wxxx>.png
=> run EMOCA (image mode)
=> outputs stored in MEAD_EMOCA/template_output/<M|Wxxx00>/mesh_coarse_detail.obj
=> store .obj in MEAD_OPEN3D/<M|Wxxx>/template.obj

// Create unregistered 3D mesh from videos ✅

MEAD/<M|Wxxx>/video-001/video/front/<emotion>/<level_1|level_2|level_3>/<xxx>.mp4
=> run EMOCA (video mode)
=> outputs stored in MEAD_EMOCA/<M|Wxxx>/<processed_xxx(latest)>/<xxx(only_one_folder)>/results/EMOCA/<xxxxxx_000>/mesh_coarse_detail.obj
=> for every .obj, store it in MEAD_OPEN3D/<M|Wxxx>/<emotion>/<level_1|level_2|level_3>/<xxx>/mesh_coarse_detail_<xxxxxx>.obj

// Grab audio from video ✅

MEAD/<M|Wxxx>/audio/<emotion>/<level_1|level_2|level_3>/<xxx>.m4a
=> convert m4a to wav
=> for every wav, store it in MEAD_FACEFORMER/wav/<M|Wxxx_emotion_(level_1|level_2|level_3)_xxx>.wav
=> `/wav`

[MEAD_OPEN3D STAGE]

// Create normalised template.obj for every subject ✅

MEAD_OPEN3D/<M|Wxxx>/template.obj
=> run mesh centering and surface area sqrt normalisation
=> outputs stored in MEAD_FACEFORMER/templates/<M|Wxxx>.obj
=> `/templates`

// Create registered 3D mesh from template and video objs ✅

MEAD_OPEN3D/<M|Wxxx>/<emotion>/<level_1|level_2|level_3>/<xxx>/mesh_coarse_detail_<xxxxxx>.obj
=> run Open3D registration, template: MEAD_FACEFORMER/templates/<M|Wxxx>.obj
=> outputs stored in MEAD_PREFORMER/<M|Wxxx>/<emotion>/<level_1|level_2|level_3>/<xxx>/mesh_coarse_detail_<xxxxxx>.obj

[MEAD_PREFORMER STAGE]

// Convert all template.obj into template.pkl ✅

MEAD_FACEFORMER/templates/<M|Wxxx>.obj
=> run script to turn all into pkl
=> store as one file in MEAD_FACEFORMER/template.pkl
=> `/template.pkl`

// Convert each .obj of a video into one .npy ✅

MEAD_PREFORMER/<M|Wxxx>/<emotion>/<level_1|level_2|level_3>/<xxx>/mesh_coarse_detail_<xxxxxx>.obj
=> for every video (<xxx>), turn all .obj into one .npy
=> store in MEAD_FACEFORMER/vertices_npy/<M|Wxxx_emotion_(level_1|level_2|level_3)_xxx>.npy
=> `/vertices_npy`
