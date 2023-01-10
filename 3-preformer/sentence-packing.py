import os
import numpy as np
import trimesh
import copy


def do_sentence_packing(BASE_DATA_PATH):
  print("3-preformer: sentence-packing start")

  # Create output directory if not exist
  OUTPUT_DIR = os.path.join(BASE_DATA_PATH, "MEAD_FACEFORMER", "vertices_npy")
  if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Output path {OUTPUT_DIR} created")

  BASE_PATH_PREFORMER = os.path.join(BASE_DATA_PATH, "MEAD_PREFORMER")

  for subject in os.listdir(BASE_PATH_PREFORMER):
    for emotion in os.listdir(os.path.join(BASE_PATH_PREFORMER, subject)):
      for level in os.listdir(os.path.join(BASE_PATH_PREFORMER, subject, emotion)):
        for video in os.listdir(os.path.join(BASE_PATH_PREFORMER, subject, emotion, level)):
          print("Processing " + os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video))
          data_verts = []
          for obj in os.listdir(os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video)):
            mesh = trimesh.load(os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video, obj))
            verts = copy.deepcopy(mesh.vertices)
            print(os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video, obj) + ", verts shape: " + str(verts.shape))
            verts = np.reshape(verts, (-1, verts.shape[0] * verts.shape[1]))
            # BUG: Not all objects from upstream have the same vertex shape
            if verts.shape[1] == 59315 * 3:
              # BUG: The order of verts being inserted into `data_verts` isn't chronological (frame by frame)
              data_verts.append(verts)
            else:
              raise Exception("An obj doesn't have the exact number of vertices")
          
          data_verts = np.array(data_verts)
          data_verts = np.squeeze(data_verts)
          file_name = f"{subject}_{emotion}_{level}_{video}.npy"
          file_path = os.path.join(OUTPUT_DIR, file_name)
          np.save(file_path, data_verts)
          print(f"Saved data_verts of shape {data_verts.shape} to {file_path}")

  print("3-preformer: sentence-packing end")

def main():
  BASE_DATA_PATH = "../test-data/"
  do_sentence_packing(BASE_DATA_PATH)

if __name__ == "__main__":
  main()