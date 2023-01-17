**BUG-1:** Incorrect mesh registration in `2-open3d/mesh-registration.py`. See `test-data/MEAD_PREFORMER/M003/angry/level_1/001/mesh_coarse_detail_000080.obj`

**SOLUTION-1**: Fixed by not doing mesh registration :) Instead, we modify EMOCA's model outputs to cancel out the rotation before it is applied to the output vertex. See `emoca/gdl/models/DecaFLAME.py, FLAME -> forward -> line 214` comment for more details.

**BUG-2:** Not all objects (either from EMOCA or mesh registration) has the same number of vertexes (59315, 3). Some have (59313, 3), some even fewer. This causes issues when doing `3-preformer/sentence-packing.py` ✅ 

**SOLUTION-2**: Assuming we only extract 'v crd_x crd_y crd_z' and read it as text file without any library


**BUG-3:** The order of `verts` being appended into `data_verts` isn't chronological (frame-by-frame). This is because `os.listdir` doesn't sort file names when providing the iterator. ✅

**SOLUTION-3**: Implemented a heap that self balances on insertion and creates a list of vertices sorted by frame number after each `.obj` iteration
