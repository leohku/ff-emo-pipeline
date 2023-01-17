import os
import numpy as np
import trimesh
import copy
import heapq
import re


def get_sorted_list_from_heap(heap):
    ordered = []
    while heap:
        ordered.append(heapq.heappop(heap))
    return ordered

def extract_vert(filepath):
  with open(filepath, "r") as file:
      # Extract the vertex data from the file
      vertex_data = [line.split()[1:4] for line in file if line.startswith("v ")]
      vertex_array = np.array(vertex_data)
      vert = np.reshape(vertex_array, (-1, vertex_array.shape[0] * vertex_array.shape[1]))
      return vert


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
            target_obj_path = os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video, obj)
            # mesh = trimesh.load(os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video, obj))
            # verts = copy.deepcopy(mesh.vertices)
            frame_count = int(obj.split(os.sep)[-1].split('_')[3].split('.')[0]) # for sorting
            verts = extract_vert(target_obj_path)
            print(os.path.join(BASE_PATH_PREFORMER, subject, emotion, level, video, obj) + ", verts shape: " + str(verts.shape))
            # BUG: Not all objects from upstream have the same vertex shape
            if verts.shape[1] == 59315 * 3:
              heapq.heappush(data_verts, (frame_count, verts))
            else:
              raise Exception("An obj doesn't have the exact number of vertices")
          # sort the vertices list by frame num
          data_verts = get_sorted_list_from_heap(data_verts)
          # remove the sorting index
          data_verts = [d[1] for d in data_verts]
          data_verts = np.array(data_verts)
          data_verts = np.squeeze(data_verts)
          file_name = f"{subject}_{emotion}_{level}_{video}.npy"
          file_path = os.path.join(OUTPUT_DIR, file_name)
          np.save(file_path, data_verts)
          print(f"Saved data_verts of shape {data_verts.shape} to {file_path}")

  print("3-preformer: sentence-packing end")

def main():
  BASE_DATA_PATH = os.environ["BASE_DATA_PATH"]
  do_sentence_packing(BASE_DATA_PATH)

if __name__ == "__main__":
  main()