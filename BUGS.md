**BUG-1:** Incorrect mesh registration in `2-open3d/mesh-registration.py`. See `test-data/MEAD_PREFORMER/M003/angry/level_1/001/mesh_coarse_detail_000080.obj`

**BUG-2:** Not all objects (either from EMOCA or mesh registration) has the same number of vertexes (59315, 3). Some have (59313, 3), some even fewer. This causes issues when doing `3-preformer/sentence-packing.py`

**BUG-3:** The order of `verts` being appended into `data_verts` isn't chronological (frame-by-frame). This is because `os.listdir` doesn't sort file names when providing the iterator.
