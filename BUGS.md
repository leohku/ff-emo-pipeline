**BUG-1:** Incorrect mesh registration in `2-open3d/mesh-registration.py`. See `test-data/MEAD_PREFORMER/M003/angry/level_1/001/mesh_coarse_detail_000080.obj`

**SOLUTION-1**: Fixed by not doing mesh registration :) Instead, we modify EMOCA's model outputs to cancel out the rotation before it is applied to the output vertex. See `emoca/gdl/models/DecaFLAME.py, FLAME -> forward -> line 214` comment for more details.

**BUG-2:** Not all objects (either from EMOCA or mesh registration) has the same number of vertexes (59315, 3). Some have (59313, 3), some even fewer. This causes issues when doing `3-preformer/sentence-packing.py` ✅ 

**SOLUTION-2**: Assuming we only extract 'v crd_x crd_y crd_z' and read it as text file without any library


**BUG-3:** The order of `verts` being appended into `data_verts` isn't chronological (frame-by-frame). This is because `os.listdir` doesn't sort file names when providing the iterator. ✅

**SOLUTION-3**: Implemented a heap that self balances on insertion and creates a list of vertices sorted by frame number after each `.obj` iteration

**BUG-4:** Each entry of template.pkl should have been an np.array

**SOLUTION-4**: Fixed

**BUG-5:** All templates and sentences vertices are packed as str instead of float. "U12" type in numpy is 48 bytes, compared to 4 bytes for float. This means the file size can be 10 times smaller than current, and RAM can store 10 times more dataset before optimising the dataloader.
In reality, the full "string" /vertices_npy folder of a subject is 56GB, while the full "float" /result (predicted vertices result, same dimension) is 1.7GB, 32x difference.

**SOLUTION-5**: Added .astype(dtype="float32") when reading the data
